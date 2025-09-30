from abc import ABC, abstractmethod
import time
import hashlib
import logging

class DataInterface(ABC):
    @abstractmethod
    def read(self, key: str) -> str:
        pass
    
    @abstractmethod
    def write(self, key: str, value: str) -> None:
        pass

class SecureStorage(DataInterface):
    def __init__(self):
        self._data = {}
        
    def read(self, key: str) -> str:
        return self._data.get(key, "")
    
    def write(self, key: str, value: str) -> None:
        self._data[key] = value

class AccessController(DataInterface):
    def __init__(self, real_storage: DataInterface, ttl: int = 300):
        self._storage = real_storage
        self._cache = {}
        self._cache_times = {}
        self._access_log = []
        self._ttl = ttl
        
    def _hash_key(self, key: str) -> str:
        return hashlib.md5(key.encode()).hexdigest()
    
    def _is_authorized(self) -> bool:
        return True
    
    def _log_access(self, operation: str, key: str):
        self._access_log.append((time.time(), operation, key))
        
    def _invalidate_cache(self, key: str):
        hkey = self._hash_key(key)
        self._cache.pop(hkey, None)
        self._cache_times.pop(hkey, None)
    
    def read(self, key: str) -> str:
        if not self._is_authorized():
            raise PermissionError("Access denied")
            
        hkey = self._hash_key(key)
        current_time = time.time()
        
        if hkey in self._cache:
            if current_time - self._cache_times[hkey] < self._ttl:
                self._log_access("READ-CACHE", key)
                return self._cache[hkey]
        
        value = self._storage.read(key)
        self._cache[hkey] = value
        self._cache_times[hkey] = current_time
        self._log_access("READ-STORAGE", key)
        return value
    
    def write(self, key: str, value: str) -> None:
        if not self._is_authorized():
            raise PermissionError("Access denied")
            
        self._storage.write(key, value)
        self._invalidate_cache(key)
        self._log_access("WRITE", key)

if __name__ == "__main__":
    storage = SecureStorage()
    controller = AccessController(storage)
    
    controller.write("user1", "sensitive_data")
    print(controller.read("user1"))
    print(controller.read("user1"))