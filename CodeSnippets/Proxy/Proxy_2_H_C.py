import weakref
import time
from abc import ABC, abstractmethod
from functools import wraps
from typing import Dict, Any, Optional

class DataService(ABC):
    @abstractmethod
    def fetch_data(self, key: str) -> str:
        pass
    
    @abstractmethod
    def update_data(self, key: str, value: str) -> bool:
        pass

class RemoteDataService(DataService):
    def __init__(self):
        self._data = {
            "user_1": "Alice Johnson",
            "user_2": "Bob Smith",
            "user_3": "Carol White"
        }
    
    def fetch_data(self, key: str) -> str:
        time.sleep(0.5)  # Simulate network delay
        if key not in self._data:
            raise KeyError(f"Key '{key}' not found")
        return self._data[key]
    
    def update_data(self, key: str, value: str) -> bool:
        time.sleep(0.3)  # Simulate network delay
        self._data[key] = value
        return True

def access_control(required_role: str = "user"):
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if not hasattr(self, '_current_user') or not self._current_user:
                raise PermissionError("Authentication required")
            user_role = getattr(self._current_user, 'role', 'guest')
            if user_role != required_role and user_role != 'admin':
                raise PermissionError(f"Access denied: {required_role} role required")
            return func(self, *args, **kwargs)
        return wrapper
    return decorator

class CachingGateway(DataService):
    _instances: Dict[int, 'CachingGateway'] = weakref.WeakValueDictionary()
    
    def __new__(cls, service: DataService):
        service_id = id(service)
        if service_id in cls._instances:
            return cls._instances[service_id]
        instance = super().__new__(cls)
        cls._instances[service_id] = instance
        return instance
    
    def __init__(self, service: DataService):
        if hasattr(self, '_initialized'):
            return
        self._service = service
        self._cache: Dict[str, tuple] = {}
        self._cache_ttl = 2.0
        self._current_user: Optional[Any] = None
        self._access_log = []
        self._initialized = True
    
    def authenticate(self, user):
        self._current_user = user
    
    @access_control("user")
    def fetch_data(self, key: str) -> str:
        current_time = time.time()
        
        if key in self._cache:
            cached_value, timestamp = self._cache[key]
            if current_time - timestamp < self._cache_ttl:
                self._log_access(f"Cache hit for key: {key}")
                return cached_value
        
        try:
            result = self._service.fetch_data(key)
            self._cache[key] = (result, current_time)
            self._log_access(f"Remote fetch for key: {key}")
            return result
        except Exception as e:
            self._log_access(f"Error fetching key {key}: {str(e)}")
            raise
    
    @access_control("admin")
    def update_data(self, key: str, value: str) -> bool:
        try:
            success = self._service.update_data(key, value)
            if success and key in self._cache:
                del self._cache[key]
            self._log_access(f"Updated key: {key}")
            return success
        except Exception as e:
            self._log_access(f"Error updating key {key}: {str(e)}")
            raise
    
    def _log_access(self, action: str):
        username = getattr(self._current_user, 'name', 'Unknown') if self._current_user else 'Anonymous'
        self._access_log.append(f"{time.strftime('%H:%M:%S')} - {username}: {action}")
    
    def get_access_log(self) -> list:
        return self._access_log.copy()

class User:
    def __init__(self, name: str, role: str):
        self.name = name
        self.role = role

if __name__ == "__main__":
    remote_service = RemoteDataService()
    gateway = CachingGateway(remote_service)
    
    user = User("Alice", "user")
    admin = User("Admin", "admin")
    
    gateway.authenticate(user)
    
    print("First fetch (cache miss):")
    start = time.time()
    data = gateway.fetch_data("user_1")
    print(f"Result: {data}, Time: {time.time() - start:.2f}s")
    
    print("\nSecond fetch (cache hit):")
    start = time.time()
    data = gateway.fetch_data("user_1")
    print(f"Result: {data}, Time: {time.time() - start:.2f}s")
    
    gateway.authenticate(admin)
    print("\nUpdating data as admin:")
    gateway.update_data("user_1", "Alice Cooper")
    
    gateway.authenticate(user)
    print("\nFetch after update:")
    data = gateway.fetch_data("user_1")
    print(f"Result: {data}")
    
    print("\nAccess log:")
    for entry in gateway.get_access_log():
        print(entry)