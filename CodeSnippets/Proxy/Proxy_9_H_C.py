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
            "user1": "Alice Johnson",
            "user2": "Bob Smith",
            "config": "production_settings"
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

class CachingServiceWrapper(DataService):
    def __init__(self, service: DataService, cache_ttl: int = 5, max_cache_size: int = 100):
        self._service = service
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._cache_ttl = cache_ttl
        self._max_cache_size = max_cache_size
        self._access_log = []
        self._lock = threading.RLock()
    
    def _is_cache_valid(self, key: str) -> bool:
        if key not in self._cache:
            return False
        return time.time() - self._cache[key]['timestamp'] < self._cache_ttl
    
    def _evict_expired_entries(self):
        current_time = time.time()
        expired_keys = [
            key for key, value in self._cache.items()
            if current_time - value['timestamp'] >= self._cache_ttl
        ]
        for key in expired_keys:
            del self._cache[key]
    
    def _enforce_cache_limit(self):
        if len(self._cache) >= self._max_cache_size:
            oldest_key = min(self._cache.keys(), key=lambda k: self._cache[k]['timestamp'])
            del self._cache[oldest_key]
    
    def fetch_data(self, key: str) -> str:
        with self._lock:
            self._evict_expired_entries()
            
            if self._is_cache_valid(key):
                self._access_log.append(f"Cache HIT for '{key}'")
                return self._cache[key]['data']
            
            try:
                self._access_log.append(f"Cache MISS for '{key}' - fetching from remote")
                data = self._service.fetch_data(key)
                
                self._enforce_cache_limit()
                self._cache[key] = {
                    'data': data,
                    'timestamp': time.time()
                }
                return data
            except Exception as e:
                self._access_log.append(f"ERROR fetching '{key}': {str(e)}")
                raise
    
    def update_data(self, key: str, value: str) -> bool:
        with self._lock:
            try:
                result = self._service.update_data(key, value)
                if result and key in self._cache:
                    del self._cache[key]
                    self._access_log.append(f"Invalidated cache for '{key}' after update")
                return result
            except Exception as e:
                self._access_log.append(f"ERROR updating '{key}': {str(e)}")
                raise
    
    def get_cache_stats(self) -> Dict[str, Any]:
        with self._lock:
            return {
                'cached_entries': len(self._cache),
                'recent_access_log': self._access_log[-10:],
                'cache_keys': list(self._cache.keys())
            }

if __name__ == "__main__":
    remote_service = RemoteDataService()
    cached_service = CachingServiceWrapper(remote_service, cache_ttl=3, max_cache_size=2)
    
    print("=== Demonstrating Caching Behavior ===")
    
    # First access - cache miss
    start_time = time.time()
    data1 = cached_service.fetch_data("user1")
    print(f"First fetch: {data1} (took {time.time() - start_time:.2f}s)")
    
    # Second access - cache hit
    start_time = time.time()
    data2 = cached_service.fetch_data("user1")
    print(f"Second fetch: {data2} (took {time.time() - start_time:.2f}s)")
    
    # Update operation
    cached_service.update_data("user1", "Alice Williams")
    
    # Fetch after update - should be cache miss
    start_time = time.time()
    data3 = cached_service.fetch_data("user1")
    print(f"After update: {data3} (took {time.time() - start_time:.2f}s)")
    
    # Test cache eviction
    cached_service.fetch_data("user2")
    cached_service.fetch_data("config")  # Should evict user1 due to size limit
    
    print("\n=== Cache Statistics ===")
    stats = cached_service.get_cache_stats()
    for key, value in stats.items():
        print(f"{key}: {value}")