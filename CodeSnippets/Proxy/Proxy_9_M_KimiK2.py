import time
from abc import ABC, abstractmethod

class StorageService(ABC):
    @abstractmethod
    def retrieve(self, key: str) -> str:
        pass

class RemoteStorage(StorageService):
    def retrieve(self, key: str) -> str:
        time.sleep(1)
        return f"Data for {key}"

class CachedStorage(StorageService):
    def __init__(self, real_storage: StorageService):
        self._real = real_storage
        self._cache = {}
        self._hits = 0
    
    def retrieve(self, key: str) -> str:
        if key in self._cache:
            self._hits += 1
            return self._cache[key]
        result = self._real.retrieve(key)
        self._cache[key] = result
        return result
    
    def get_cache_stats(self) -> dict:
        return {"cached_keys": list(self._cache.keys()), "cache_hits": self._hits}

if __name__ == "__main__":
    remote = RemoteStorage()
    cached = CachedStorage(remote)
    
    print(cached.retrieve("user:123"))
    print(cached.retrieve("user:123"))
    print(cached.retrieve("config:main"))
    print(cached.get_cache_stats())