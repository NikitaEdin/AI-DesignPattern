import weakref
from abc import ABC, abstractmethod
from functools import wraps
import time
import threading

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
            "config_main": "production_settings"
        }
    
    def fetch_data(self, key: str) -> str:
        time.sleep(0.1)  # Simulate network delay
        if key not in self._data:
            raise ValueError(f"Key '{key}' not found")
        return self._data[key]
    
    def update_data(self, key: str, value: str) -> bool:
        time.sleep(0.1)  # Simulate network delay
        self._data[key] = value
        return True

class CachingServiceWrapper(DataService):
    _instances = weakref.WeakValueDictionary()
    _lock = threading.RLock()
    
    def __new__(cls, service_instance):
        service_id = id(service_instance)
        with cls._lock:
            if service_id in cls._instances:
                return cls._instances[service_id]
            instance = super().__new__(cls)
            cls._instances[service_id] = instance
            return instance
    
    def __init__(self, service_instance):
        if hasattr(self, '_initialized'):
            return
        self._service = service_instance
        self._cache = {}
        self._cache_times = {}
        self._access_log = []
        self._cache_ttl = 5.0
        self._max_cache_size = 10
        self._initialized = True
    
    def _log_access(method_name: str, key: str):
        def decorator(func):
            @wraps(func)
            def wrapper(self, *args, **kwargs):
                with self._lock:
                    self._access_log.append({
                        'method': method_name,
                        'key': key if isinstance(key, str) else args[0],
                        'timestamp': time.time()
                    })
                    if len(self._access_log) > 50:
                        self._access_log = self._access_log[-25:]
                return func(self, *args, **kwargs)
            return wrapper
        return decorator
    
    def _is_cache_valid(self, key: str) -> bool:
        if key not in self._cache_times:
            return False
        return time.time() - self._cache_times[key] < self._cache_ttl
    
    def _evict_if_needed(self):
        if len(self._cache) >= self._max_cache_size:
            oldest_key = min(self._cache_times.keys(), 
                           key=lambda k: self._cache_times[k])
            del self._cache[oldest_key]
            del self._cache_times[oldest_key]
    
    @_log_access("fetch", "key")
    def fetch_data(self, key: str) -> str:
        with self._lock:
            if self._is_cache_valid(key):
                return self._cache[key]
            
            try:
                data = self._service.fetch_data(key)
                self._evict_if_needed()
                self._cache[key] = data
                self._cache_times[key] = time.time()
                return data
            except Exception as e:
                if key in self._cache:
                    return self._cache[key]
                raise e
    
    @_log_access("update", "key")
    def update_data(self, key: str, value: str) -> bool:
        with self._lock:
            result = self._service.update_data(key, value)
            if result:
                self._cache[key] = value
                self._cache_times[key] = time.time()
            return result
    
    def get_cache_stats(self) -> dict:
        with self._lock:
            return {
                'cache_size': len(self._cache),
                'recent_accesses': len(self._access_log),
                'cached_keys': list(self._cache.keys())
            }

if __name__ == "__main__":
    remote_service = RemoteDataService()
    
    wrapper1 = CachingServiceWrapper(remote_service)
    wrapper2 = CachingServiceWrapper(remote_service)
    
    print("Singleton check:", wrapper1 is wrapper2)
    
    print("First fetch (cache miss):")
    start = time.time()
    result = wrapper1.fetch_data("user_1")
    print(f"Result: {result}, Time: {time.time() - start:.3f}s")
    
    print("\nSecond fetch (cache hit):")
    start = time.time()
    result = wrapper1.fetch_data("user_1")
    print(f"Result: {result}, Time: {time.time() - start:.3f}s")
    
    print("\nUpdate data:")
    wrapper1.update_data("user_1", "Alice Williams")
    result = wrapper1.fetch_data("user_1")
    print(f"Updated result: {result}")
    
    print(f"\nCache stats: {wrapper1.get_cache_stats()}")