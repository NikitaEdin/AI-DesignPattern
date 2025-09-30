import threading
import time
from typing import Optional

class SharedResource:

    _lock = threading.RLock()
    _instance: Optional['SharedResource'] = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, value: int = 0):
        if not hasattr(self, '_initialized'):
            self._value = value
            self._initialized = True

    def set_value(self, value: int):
        self._value = value

    def get_value(self) -> int:
        return self._value

    def __reduce__(self):
        raise TypeError("Cannot serialize SharedResource")

class DerivedResource(SharedResource):

    def __init__(self, value: int = 0, name: str = "default"):
        super().__init__(value)
        if not hasattr(self, '_name'):
            self._name = name

    def get_name(self) -> str:
        return self._name

if __name__ == "__main__":
    def worker(n: int):
        obj = SharedResource(n)
        time.sleep(0.1)
        obj.set_value(obj.get_value() + 10)
        print(f"Thread {n}: {obj.get_value()}")

    threads = [threading.Thread(target=worker, args=(i,)) for i in range(5)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    a = SharedResource(5)
    b = SharedResource(10)
    print("Same instance:", a is b)
    print("Final value:", a.get_value())

    c = DerivedResource(42, "special")
    d = DerivedResource(99, "ignored")
    print("Derived same:", c is d)
    print("Derived value:", c.get_value())
    print("Derived name:", c.get_name())