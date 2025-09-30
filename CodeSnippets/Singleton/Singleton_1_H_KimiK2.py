import threading
import time
from functools import wraps

class AppCore:
    _lock = threading.RLock()
    _instance = None

    def __init__(self):
        raise RuntimeError("Use instance() to create")

    @classmethod
    def instance(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls.__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            return cls.instance()
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self._state = {}
        self._observers = []

    def set(self, key, value):
        self._state[key] = value
        self._notify(key, value)

    def get(self, key, default=None):
        return self._state.get(key, default)

    def register(self, callback):
        self._observers.append(callback)

    def _notify(self, key, value):
        for cb in self._observers:
            cb(key, value)

    def __reduce__(self):
        return (self.__class__, (), None, self.__iter__(), self.__dict__.copy())

    def __iter__(self):
        return iter([])

    def __copy__(self):
        return self

    def __deepcopy__(self, memo):
        return self

def synchronized(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        with AppCore._lock:
            return func(*args, **kwargs)
    return wrapper

class Service:
    def __init__(self):
        self.core = AppCore.instance()
        self.core.register(self._on_change)

    def _on_change(self, key, value):
        print(f"[{threading.current_thread().name}] {key} updated to {value}")

if __name__ == "__main__":
    def worker(n):
        core = AppCore.instance()
        for i in range(3):
            core.set(f"worker{n}_key", i)
            time.sleep(0.01)

    threads = [threading.Thread(target=worker, args=(i,)) for i in range(3)]
    svc = Service()
    [t.start() for t in threads]
    [t.join() for t in threads]
    final = AppCore.instance()
    print("Same object?", final is svc.core)
    print("Final state:", dict(final._state))