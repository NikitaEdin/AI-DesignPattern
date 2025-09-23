from abc import ABC, abstractmethod
import time
import weakref
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
            "user1": "Alice Johnson",
            "user2": "Bob Smith", 
            "user3": "Charlie Brown"
        }
        self._access_count = 0
    
    def fetch_data(self, key: str) -> str:
        self._access_count += 1
        time.sleep(0.1)  # Simulate network delay
        if key in self._data:
            return self._data[key]
        raise KeyError(f"Data not found for key: {key}")
    
    def update_data(self, key: str, value: str) -> bool:
        self._access_count += 1
        time.sleep(0.1)  # Simulate network delay
        self._data[key] = value
        return True
    
    @property
    def access_count(self) -> int:
        return self._access_count

class Guardian(DataService):
    _instances: Dict[str, 'Guardian'] = {}
    _cache_ttl = 5.0
    
    def __new__(cls, user_role: str = "user"):
        if user_role not in cls._instances:
            instance = super().__new__(cls)
            cls._instances[user_role] = instance
        return cls._instances[user_role]
    
    def __init__(self, user_role: str = "user"):
        if hasattr(self, '_initialized'):
            return
        
        self._service = RemoteDataService()
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._user_role = user_role
        self._access_log = []
        self._initialized = True
    
    def _log_access(self, operation: str, key: str, success: bool):
        self._access_log.append({
            'timestamp': time.time(),
            'operation': operation,
            'key': key,
            'success': success,
            'role': self._user_role
        })
    
    def _is_authorized(self, operation: str, key: str) -> bool:
        if self._user_role == "admin":
            return True
        if operation == "fetch" and key.startswith("user"):
            return True
        if operation == "update" and self._user_role == "editor":
            return True
        return False
    
    def _get_cached_data(self, key: str) -> Optional[str]:
        if key in self._cache:
            cache_entry = self._cache[key]
            if time.time() - cache_entry['timestamp'] < self._cache_ttl:
                return cache_entry['data']
            else:
                del self._cache[key]
        return None
    
    def _cache_data(self, key: str, data: str):
        self._cache[key] = {
            'data': data,
            'timestamp': time.time()
        }
    
    def fetch_data(self, key: str) -> str:
        if not self._is_authorized("fetch", key):
            self._log_access("fetch", key, False)
            raise PermissionError(f"Access denied for key: {key}")
        
        cached_data = self._get_cached_data(key)
        if cached_data is not None:
            self._log_access("fetch", key, True)
            return cached_data
        
        try:
            data = self._service.fetch_data(key)
            self._cache_data(key, data)
            self._log_access("fetch", key, True)
            return data
        except KeyError as e:
            self._log_access("fetch", key, False)
            raise e
    
    def update_data(self, key: str, value: str) -> bool:
        if not self._is_authorized("update", key):
            self._log_access("update", key, False)
            raise PermissionError(f"Update denied for key: {key}")
        
        try:
            result = self._service.update_data(key, value)
            if result and key in self._cache:
                del self._cache[key]
            self._log_access("update", key, result)
            return result
        except Exception as e:
            self._log_access("update", key, False)
            raise e
    
    @property
    def cache_size(self) -> int:
        return len(self._cache)
    
    @property
    def access_log(self) -> list:
        return self._access_log.copy()

if __name__ == "__main__":
    user_guardian = Guardian("user")
    admin_guardian = Guardian("admin")
    
    print("User accessing data:")
    print(user_guardian.fetch_data("user1"))
    print(user_guardian.fetch_data("user1"))  # Should use cache
    
    print("\nAdmin accessing data:")
    print(admin_guardian.fetch_data("user2"))
    admin_guardian.update_data("user2", "Robert Smith")
    print(admin_guardian.fetch_data("user2"))
    
    print(f"\nCache size: {user_guardian.cache_size}")
    print(f"Access log entries: {len(user_guardian.access_log)}")
    
    try:
        user_guardian.update_data("user1", "New Name")
    except PermissionError as e:
        print(f"Permission error: {e}")