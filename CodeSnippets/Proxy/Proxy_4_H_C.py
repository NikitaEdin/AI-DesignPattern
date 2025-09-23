import time
import threading
from abc import ABC, abstractmethod
from functools import wraps
from typing import Any, Dict, Optional

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
            "config_timeout": "30",
            "config_retries": "3"
        }
    
    def fetch_data(self, key: str) -> str:
        time.sleep(0.5)  # Simulate network latency
        return self._data.get(key, "Not found")
    
    def update_data(self, key: str, value: str) -> bool:
        time.sleep(0.3)  # Simulate network latency
        self._data[key] = value
        return True

class CachedServiceGateway(DataService):
    def __init__(self, service: DataService, cache_ttl: int = 10, max_retries: int = 3):
        self._service = service
        self._cache: Dict[str, Any] = {}
        self._cache_timestamps: Dict[str, float] = {}
        self._cache_ttl = cache_ttl
        self._max_retries = max_retries
        self._lock = threading.RLock()
        self._access_log: Dict[str, int] = {}
    
    def _is_cache_valid(self, key: str) -> bool:
        if key not in self._cache_timestamps:
            return False
        return time.time() - self._cache_timestamps[key] < self._cache_ttl
    
    def _log_access(self, key: str):
        with self._lock:
            self._access_log[key] = self._access_log.get(key, 0) + 1
    
    def _retry_on_failure(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(self._max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == self._max_retries - 1:
                        raise e
                    time.sleep(0.1 * (attempt + 1))
            return None
        return wrapper
    
    def fetch_data(self, key: str) -> str:
        self._log_access(key)
        
        with self._lock:
            if self._is_cache_valid(key):
                return self._cache[key]
        
        @self._retry_on_failure
        def _fetch():
            return self._service.fetch_data(key)
        
        result = _fetch()
        
        with self._lock:
            self._cache[key] = result
            self._cache_timestamps[key] = time.time()
        
        return result
    
    def update_data(self, key: str, value: str) -> bool:
        self._log_access(key)
        
        @self._retry_on_failure
        def _update():
            return self._service.update_data(key, value)
        
        success = _update()
        
        if success:
            with self._lock:
                self._cache[key] = value
                self._cache_timestamps[key] = time.time()
        
        return success
    
    def get_cache_stats(self) -> Dict[str, Any]:
        with self._lock:
            return {
                "cached_items": len(self._cache),
                "access_log": self._access_log.copy(),
                "cache_keys": list(self._cache.keys())
            }
    
    def clear_cache(self):
        with self._lock:
            self._cache.clear()
            self._cache_timestamps.clear()

if __name__ == "__main__":
    remote_service = RemoteDataService()
    gateway = CachedServiceGateway(remote_service, cache_ttl=5, max_retries=2)
    
    print("First fetch (cache miss):")
    start = time.time()
    result1 = gateway.fetch_data("user_1")
    print(f"Result: {result1}, Time: {time.time() - start:.2f}s")
    
    print("\nSecond fetch (cache hit):")
    start = time.time()
    result2 = gateway.fetch_data("user_1")
    print(f"Result: {result2}, Time: {time.time() - start:.2f}s")
    
    print("\nUpdating data:")
    gateway.update_data("user_1", "Alice Williams")
    result3 = gateway.fetch_data("user_1")
    print(f"Updated result: {result3}")
    
    print(f"\nCache statistics: {gateway.get_cache_stats()}")