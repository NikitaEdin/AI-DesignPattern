from typing import Protocol
import time
import threading
from functools import wraps

class Resource(Protocol):
    def request(self, key: str) -> str: ...
    def update(self, key: str, value: str) -> None: ...

class RealResource:
    def __init__(self):
        self._data = {}
        self._lock = threading.Lock()
    
    def request(self, key: str) -> str:
        with self._lock:
            time.sleep(0.2)
            return self._data.get(key, "<not found>")
    
    def update(self, key: str, value: str) -> None:
        with self._lock:
            time.sleep(0.2)
            self._data[key] = value

class CachedAccess:
    def __init__(self, subject: RealResource, max_age: float = 1.0):
        self._subject = subject
        self._cache = {}
        self._timestamps = {}
        self._max_age = max_age
        self._lock = threading.Lock()
    
    def _is_fresh(self, key: str) -> bool:
        return key in self._timestamps and (time.time() - self._timestamps[key]) < self._max_age
    
    def request(self, key: str) -> str:
        with self._lock:
            if self._is_fresh(key):
                return self._cache[key]
            value = self._subject.request(key)
            self._cache[key] = value
            self._timestamps[key] = time.time()
            return value
    
    def update(self, key: str, value: str) -> None:
        with self._lock:
            self._subject.update(key, value)
            self._cache.pop(key, None)
            self._timestamps.pop(key, None)

class SecuredAccess:
    def __init__(self, subject: Resource, allowed_users: set[str]):
        self._subject = subject
        self._users = allowed_users
    
    def _authenticate(self):
        if threading.current_thread().name not in self._users:
            raise PermissionError("Access denied")
    
    def request(self, key: str) -> str:
        self._authenticate()
        return self._subject.request(key)
    
    def update(self, key: str, value: str) -> None:
        self._authenticate()
        self._subject.update(key, value)

if __name__ == "__main__":
    core = RealResource()
    core.update("alpha", "initial")
    
    cached = CachedAccess(core, max_age=0.5)
    secured = SecuredAccess(cached, allowed_users={"MainThread"})
    
    print(secured.request("alpha"))
    
    secured.update("alpha", "updated")
    assert secured.request("alpha") == "updated"
    
    def rogue():
        try:
            secured.request("alpha")
        except PermissionError as e:
            print("Blocked:", e)
    
    threading.Thread(target=rogue, name="Intruder").start()