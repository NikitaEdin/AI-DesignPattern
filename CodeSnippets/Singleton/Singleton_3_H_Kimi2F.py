import threading
import weakref
from functools import wraps

class _Meta(type):
    _lock = threading.RLock()
    _instances = weakref.WeakValueDictionary()

    def __call__(cls, *a, **kw):
        if cls in cls._instances:
            return cls._instances[cls]
        with cls._lock:
            if cls not in cls._instances:
                inst = super().__call__(*a, **kw)
                cls._instances[cls] = inst
            return cls._instances[cls]

class Database(metaclass=_Meta):
    def __init__(self):
        if hasattr(self, '_initialized'):
            return
        self._initialized = True
        self._data = {}
        self._lock = threading.RLock()

    def store(self, key, value):
        with self._lock:
            self._data[key] = value

    def fetch(self, key):
        with self._lock:
            return self._data.get(key)

    def __repr__(self):
        with self._lock:
            return f"<Database {dict(self._data)}>"

class Logger:
    _holder = None
    _lock = threading.RLock()

    def __new__(cls):
        if cls._holder is None:
            with cls._lock:
                if cls._holder is None:
                    cls._holder = super().__new__(cls)
                    cls._holder._log = []
        return cls._holder

    def add(self, msg):
        self._log.append(msg)

    def dump(self):
        return tuple(self._log)

def synchronize(method):
    @wraps(method)
    def wrapper(self, *a, **kw):
        with self._lock:
            return method(self, *a, **kw)
    return wrapper

class Cache:
    def __init__(self):
        raise RuntimeError("Use instance()")

    @classmethod
    def instance(cls):
        if not hasattr(cls, '_inst'):
            with cls._lock:
                if not hasattr(cls, '_inst'):
                    cls._inst = cls.__new__(cls)
                    cls._inst._cache = {}
        return cls._inst

    def set(self, k, v):
        with self._lock:
            self._cache[k] = v

    def get(self, k):
        with self._lock:
            return self._cache.get(k)

    _lock = threading.RLock()

if __name__ == "__main__":
    d1 = Database()
    d2 = Database()
    d1.store("A", 1)
    print(d2.fetch("A"))  # 1
    print(d1 is d2)       # True

    l1 = Logger()
    l2 = Logger()
    l1.add("hello")
    print(l2.dump())      # ('hello',)
    print(l1 is l2)       # True

    c1 = Cache.instance()
    c2 = Cache.instance()
    c1.set("X", 99)
    print(c2.get("X"))    # 99
    print(c1 is c2)       # True