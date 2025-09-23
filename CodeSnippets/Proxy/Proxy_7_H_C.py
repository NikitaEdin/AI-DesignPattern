import time
import threading
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
            "user_1": "John Doe",
            "user_2": "Jane Smith",
            "user_3": "Bob Johnson"
        }
    
    def fetch_data(self, key: str) -> str:
        time.sleep(0.5)
        return self._data.get(key, "Not found")
    
    def update_data(self, key: str, value: str) -> bool:
        time.sleep(0.3)
        self._data[key] = value
        return True

class CachingGateway(DataService):
    def __init__(self, service: DataService, cache_ttl: int = 5):
        self._service = service
        self._cache: Dict[str, Any] = {}
        self._cache_timestamps: Dict[str, float] = {}
        self._cache_ttl = cache_ttl
        self._lock = threading.RLock()
        self._access_count = 0
        self._authorized_keys = {"user_1", "user_2", "user_3", "admin"}
    
    def _is_cache_valid(self, key: str) -> bool:
        if key not in self._cache_timestamps:
            return False
        return time.time() - self._cache_timestamps[key] < self._cache_ttl
    
    def _check_authorization(self, key: str) -> bool:
        return key in self._authorized_keys
    
    def _log_access(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            with self._lock:
                self._access_count += 1
                return func(self, *args, **kwargs)
        return wrapper
    
    @_log_access
    def fetch_data(self, key: str) -> str:
        if not self._check_authorization(key):
            return "Access denied"
        
        with self._lock:
            if self._is_cache_valid(key):
                return f"[CACHED] {self._cache[key]}"
            
            result = self._service.fetch_data(key)
            self._cache[key] = result
            self._cache_timestamps[key] = time.time()
            return f"[FRESH] {result}"
    
    @_log_access
    def update_data(self, key: str, value: str) -> bool:
        if not self._check_authorization(key):
            return False
        
        with self._lock:
            success = self._service.update_data(key, value)
            if success and key in self._cache:
                del self._cache[key]
                del self._cache_timestamps[key]
            return success
    
    def get_stats(self) -> Dict[str, Any]:
        with self._lock:
            return {
                "access_count": self._access_count,
                "cache_size": len(self._cache),
                "cached_keys": list(self._cache.keys())
            }

if __name__ == "__main__":
    remote_service = RemoteDataService()
    gateway = CachingGateway(remote_service, cache_ttl=3)
    
    print("First fetch (fresh):", gateway.fetch_data("user_1"))
    print("Second fetch (cached):", gateway.fetch_data("user_1"))
    
    print("Unauthorized access:", gateway.fetch_data("user_999"))
    
    print("Update:", gateway.update_data("user_1", "John Updated"))
    print("After update (cache invalidated):", gateway.fetch_data("user_1"))
    
    time.sleep(4)
    print("After cache expiry:", gateway.fetch_data("user_1"))
    
    print("Statistics:", gateway.get_stats())