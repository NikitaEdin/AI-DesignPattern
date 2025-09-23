import time
import threading
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from functools import wraps

class DataService(ABC):
    @abstractmethod
    def fetch_user_data(self, user_id: int) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    def update_user_data(self, user_id: int, data: Dict[str, Any]) -> bool:
        pass

class RemoteDataService(DataService):
    def __init__(self):
        self._connection_count = 0
    
    def fetch_user_data(self, user_id: int) -> Dict[str, Any]:
        self._connection_count += 1
        time.sleep(0.5)  # Simulate network delay
        return {
            "id": user_id,
            "name": f"User{user_id}",
            "email": f"user{user_id}@example.com",
            "timestamp": time.time()
        }
    
    def update_user_data(self, user_id: int, data: Dict[str, Any]) -> bool:
        self._connection_count += 1
        time.sleep(0.3)
        return True
    
    @property
    def connection_count(self) -> int:
        return self._connection_count

class CachingServiceWrapper(DataService):
    def __init__(self, service: DataService, cache_ttl: int = 30):
        self._service = service
        self._cache: Dict[int, Dict[str, Any]] = {}
        self._cache_timestamps: Dict[int, float] = {}
        self._cache_ttl = cache_ttl
        self._lock = threading.RLock()
        self._access_log: Dict[int, int] = {}
    
    def _is_cache_valid(self, user_id: int) -> bool:
        if user_id not in self._cache_timestamps:
            return False
        return time.time() - self._cache_timestamps[user_id] < self._cache_ttl
    
    def _log_access(self, user_id: int):
        self._access_log[user_id] = self._access_log.get(user_id, 0) + 1
    
    def fetch_user_data(self, user_id: int) -> Dict[str, Any]:
        with self._lock:
            self._log_access(user_id)
            
            if self._is_cache_valid(user_id):
                return self._cache[user_id].copy()
            
            data = self._service.fetch_user_data(user_id)
            self._cache[user_id] = data.copy()
            self._cache_timestamps[user_id] = time.time()
            return data
    
    def update_user_data(self, user_id: int, data: Dict[str, Any]) -> bool:
        with self._lock:
            result = self._service.update_user_data(user_id, data)
            if result and user_id in self._cache:
                del self._cache[user_id]
                del self._cache_timestamps[user_id]
            return result
    
    def get_access_stats(self) -> Dict[str, Any]:
        with self._lock:
            return {
                "cached_users": len(self._cache),
                "access_log": self._access_log.copy(),
                "total_accesses": sum(self._access_log.values())
            }
    
    def clear_cache(self):
        with self._lock:
            self._cache.clear()
            self._cache_timestamps.clear()

if __name__ == "__main__":
    remote_service = RemoteDataService()
    cached_service = CachingServiceWrapper(remote_service, cache_ttl=2)
    
    print("First access (cache miss):")
    start = time.time()
    user_data = cached_service.fetch_user_data(1)
    print(f"Time: {time.time() - start:.2f}s")
    print(f"Data: {user_data}")
    
    print("\nSecond access (cache hit):")
    start = time.time()
    user_data = cached_service.fetch_user_data(1)
    print(f"Time: {time.time() - start:.2f}s")
    print(f"Data: {user_data}")
    
    print(f"\nConnection count: {remote_service.connection_count}")
    print(f"Access stats: {cached_service.get_access_stats()}")
    
    cached_service.update_user_data(1, {"name": "Updated User"})
    
    print("\nAfter update (cache invalidated):")
    start = time.time()
    user_data = cached_service.fetch_user_data(1)
    print(f"Time: {time.time() - start:.2f}s")
    print(f"Final stats: {cached_service.get_access_stats()}")