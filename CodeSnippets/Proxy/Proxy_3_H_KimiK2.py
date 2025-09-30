import time
import logging
from abc import ABC, abstractmethod
from functools import wraps

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("access")

class DataInterface(ABC):
    @abstractmethod
    def retrieve(self, key): pass

class DataService(DataInterface):
    def __init__(self):
        self._store = {"a": 1, "b": 2, "c": 3}
    def retrieve(self, key):
        time.sleep(0.5)
        return self._store.get(key, None)

class ControlledAccess(DataInterface):
    def __init__(self, service: DataService):
        self._service = service
        self._cache = {}
        self._blacklist = set()
    def retrieve(self, key):
        if key in self._blacklist:
            raise PermissionError("Key blocked")
        if key in self._cache:
            logger.info("Cache hit: %s", key)
            return self._cache[key]
        logger.info("Accessing backend: %s", key)
        result = self._service.retrieve(key)
        if result is not None:
            self._cache[key] = result
        return result
    def block(self, key):
        self._blacklist.add(key)
        self._cache.pop(key, None)
    def purge(self):
        self._cache.clear()

class ThrottledAccess(DataInterface):
    def __init__(self, inner: ControlledAccess, max_calls=5, window=1):
        self.inner = inner
        self.max_calls = max_calls
        self.window = window
        self._calls = []
    def _clean(self):
        cutoff = time.time() - self.window
        self._calls = [t for t in self._calls if t > cutoff]
    def _can_pass(self):
        self._clean()
        return len(self._calls) < self.max_calls
    def retrieve(self, key):
        if not self._can_pass():
            raise RuntimeError("Too many calls")
        self._calls.append(time.time())
        return self.inner.retrieve(key)
    def block(self, key):
        self.inner.block(key)
    def purge(self):
        self.inner.purge()

if __name__ == "__main__":
    backend = DataService()
    access = ControlledAccess(backend)
    throttled = ThrottledAccess(access, max_calls=3)
    print("Fetch 'a':", throttled.retrieve("a"))
    print("Fetch 'b':", throttled.retrieve("b"))
    access.block("b")
    try:
        print(throttled.retrieve("b"))
    except PermissionError as e:
        print("Blocked:", e)
    access.purge()
    print("Fetch 'c':", throttled.retrieve("c"))