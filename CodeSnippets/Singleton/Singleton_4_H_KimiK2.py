import threading
import time
from functools import wraps

class Meta(type):
    _lock = threading.Lock()
    _map  = {}

    def __call__(cls, *a, **kw):
        if cls not in cls._map:
            with cls._lock:
                if cls not in cls._map:
                    cls._map[cls] = super().__call__(*a, **kw)
        return cls._map[cls]

class Logger(metaclass=Meta):
    def __init__(self):
        self._buffer = []
        self._writers = 0
        self._lock = threading.RLock()

    def _guard(func):
        @wraps(func)
        def _w(self, *a, **kw):
            with self._lock:
                return func(self, *a, **kw)
        return _w

    @_guard
    def write(self, msg: str):
        self._buffer.append(f"{time.time():.3f} {msg}")

    @_guard
    def dump(self):
        return self._buffer.copy()

    @_guard
    def reset(self):
        self._buffer.clear()

    def __copy__(self):
        return self
    def __deepcopy__(self, _):
        return self

class Cache(metaclass=Meta):
    def __init__(self):
        self._store = {}
        self._lock = threading.Lock()

    def set(self, k, v):
        with self._lock:
            self._store[k] = v

    def get(self, k, default=None):
        with self._lock:
            return self._store.get(k, default)

if __name__ == "__main__":
    def worker(n):
        log = Logger()
        cache = Cache()
        log.write(f"worker {n} start")
        cache.set(f"key{n}", n*10)
        time.sleep(0.01)
        log.write(f"worker {n} read {cache.get('key1')}")
        log.write(f"worker {n} done")

    threads = [threading.Thread(target=worker, args=(i,)) for i in range(3)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    print("Log contents:", Logger().dump())