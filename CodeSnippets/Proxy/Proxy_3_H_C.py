import time
import threading
from abc import ABC, abstractmethod
from functools import wraps
from typing import Any, Dict, Optional

class DataService(ABC):
    @abstractmethod
    def fetch_user_data(self, user_id: int) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    def update_user_data(self, user_id: int, data: Dict[str, Any]) -> bool:
        pass

class RemoteDataService(DataService):
    def __init__(self):
        self._users_db = {
            1: {"name": "Alice", "email": "alice@example.com", "role": "admin"},
            2: {"name": "Bob", "email": "bob@example.com", "role": "user"},
            3: {"name": "Charlie", "email": "charlie@example.com", "role": "user"}
        }
    
    def fetch_user_data(self, user_id: int) -> Dict[str, Any]:
        time.sleep(0.5)
        if user_id not in self._users_db:
            raise ValueError(f"User {user_id} not found")
        return self._users_db[user_id].copy()
    
    def update_user_data(self, user_id: int, data: Dict[str, Any]) -> bool:
        time.sleep(0.3)
        if user_id not in self._users_db:
            return False
        self._users_db[user_id].update(data)
        return True

class CachingGuard(DataService):
    def __init__(self, service: DataService, cache_ttl: int = 30):
        self._service = service
        self._cache_ttl = cache_ttl
        self._cache: Dict[int, Dict[str, Any]] = {}
        self._cache_timestamps: Dict[int, float] = {}
        self._lock = threading.RLock()
    
    def _is_cache_valid(self, user_id: int) -> bool:
        if user_id not in self._cache_timestamps:
            return False
        return time.time() - self._cache_timestamps[user_id] < self._cache_ttl
    
    def fetch_user_data(self, user_id: int) -> Dict[str, Any]:
        with self._lock:
            if self._is_cache_valid(user_id):
                return self._cache[user_id].copy()
            
            try:
                data = self._service.fetch_user_data(user_id)
                self._cache[user_id] = data.copy()
                self._cache_timestamps[user_id] = time.time()
                return data
            except Exception as e:
                if user_id in self._cache:
                    return self._cache[user_id].copy()
                raise e
    
    def update_user_data(self, user_id: int, data: Dict[str, Any]) -> bool:
        with self._lock:
            result = self._service.update_user_data(user_id, data)
            if result and user_id in self._cache:
                self._cache[user_id].update(data)
                self._cache_timestamps[user_id] = time.time()
            return result
    
    def invalidate_cache(self, user_id: Optional[int] = None):
        with self._lock:
            if user_id is None:
                self._cache.clear()
                self._cache_timestamps.clear()
            else:
                self._cache.pop(user_id, None)
                self._cache_timestamps.pop(user_id, None)

if __name__ == "__main__":
    remote_service = RemoteDataService()
    guarded_service = CachingGuard(remote_service, cache_ttl=5)
    
    print("First fetch (cache miss):")
    start = time.time()
    user_data = guarded_service.fetch_user_data(1)
    print(f"Data: {user_data}, Time: {time.time() - start:.2f}s")
    
    print("\nSecond fetch (cache hit):")
    start = time.time()
    user_data = guarded_service.fetch_user_data(1)
    print(f"Data: {user_data}, Time: {time.time() - start:.2f}s")
    
    print("\nUpdating user data:")
    guarded_service.update_user_data(1, {"name": "Alice Smith"})
    
    print("\nFetch after update (cached):")
    start = time.time()
    user_data = guarded_service.fetch_user_data(1)
    print(f"Data: {user_data}, Time: {time.time() - start:.2f}s")
    
    print("\nCache invalidation and refetch:")
    guarded_service.invalidate_cache(1)
    start = time.time()
    user_data = guarded_service.fetch_user_data(1)
    print(f"Data: {user_data}, Time: {time.time() - start:.2f}s")