import time
import threading
from abc import ABC, abstractmethod
from typing import Optional, Any
import hashlib
import weakref


class DataAccessor(ABC):
    @abstractmethod
    def fetch(self, key: str) -> Any:
        pass


class RemoteDataAccessor(DataAccessor):
    def __init__(self):
        self.call_count = 0
    
    def fetch(self, key: str) -> str:
        self.call_count += 1
        time.sleep(0.05)
        return f"Data for {key} from remote server"


class CachedDataAccessor(DataAccessor):
    def __init__(self, real_accessor: RemoteDataAccessor, ttl_seconds: int = 2):
        self._real = real_accessor
        self._ttl = ttl_seconds
        self._cache = {}
        self._timestamps = {}
        self._lock = threading.RLock()
        self._access_times = {}
        self._max_calls = 5
        self._window_seconds = 1
    
    def fetch(self, key: str) -> str:
        with self._lock:
            self._enforce_rate_limit()
            cached_value = self._get_cached(key)
            if cached_value is not None:
                return cached_value
            value = self._real.fetch(key)
            self._store_in_cache(key, value)
            return value
    
    def _get_cached(self, key: str) -> Optional[str]:
        current_time = time.time()
        if key in self._cache:
            if current_time - self._timestamps[key] < self._ttl:
                return self._cache[key]
            else:
                del self._cache[key]
                del self._timestamps[key]
        return None
    
    def _store_in_cache(self, key: str, value: str):
        current_time = time.time()
        self._cache[key] = value
        self._timestamps[key] = current_time
    
    def _enforce_rate_limit(self):
        current_time = time.time()
        self._access_times[current_time] = self._access_times.get(current_time, 0) + 1
        cutoff_time = current_time - self._window_seconds
        self._access_times = {t: c for t, c in self._access_times.items() if t > cutoff_time}
        total_calls = sum(self._access_times.values())
        if total_calls > self._max_calls:
            raise Exception("Rate limit exceeded")


if __name__ == "__main__":
    real_accessor = RemoteDataAccessor()
    cached_accessor = CachedDataAccessor(real_accessor)
    
    def access_data(accessor, key):
        try:
            result = accessor.fetch(key)
            print(f"Got: {result}")
        except Exception as e:
            print(f"Error: {e}")
    
    threads = []
    for i in range(8):
        thread = threading.Thread(target=access_data, args=(cached_accessor, f"resource_{i}"))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    
    print(f"Real accessor called {real_accessor.call_count} times")