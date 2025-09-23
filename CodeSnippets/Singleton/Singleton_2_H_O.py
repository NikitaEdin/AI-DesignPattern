import threading
import pickle
import copy
import time

class UniqueInstanceMeta(type):
    _instances = {}
    _locks = {}

    def __call__(cls, *args, **kwargs):
        if cls not in UniqueInstanceMeta._instances:
            lock = UniqueInstanceMeta._locks.setdefault(cls, threading.Lock())
            with lock:
                if cls not in UniqueInstanceMeta._instances:
                    instance = super().__call__(*args, **kwargs)
                    UniqueInstanceMeta._instances[cls] = instance
        return UniqueInstanceMeta._instances[cls]

def _get_existing(cls):
    return cls()

class ResourceManager(metaclass=UniqueInstanceMeta):
    def __init__(self, initial=None):
        if getattr(self, "_initialized", False):
            return
        self._lock = threading.RLock()
        self._value = initial
        self._initialized = True

    def set_value(self, v):
        with self._lock:
            self._value = v

    def get_value(self):
        with self._lock:
            return self._value

    def __copy__(self):
        return self

    def __deepcopy__(self, memo):
        return self

    def __reduce__(self):
        return (_get_existing, (self.__class__,))

def _thread_worker(index, barrier):
    barrier.wait()
    inst = ResourceManager(index)
    inst.set_value(index)
    print(f"thread {index} id={id(inst)} value={inst.get_value()}")

if __name__ == "__main__":
    a = ResourceManager(1)
    b = ResourceManager(2)
    print("a id:", id(a))
    print("b id:", id(b))
    print("a value:", a.get_value())
    print("b value:", b.get_value())
    print("same instance:", a is b)

    barrier = threading.Barrier(5)
    threads = [threading.Thread(target=_thread_worker, args=(i, barrier)) for i in range(5)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    print("final value after threads:", a.get_value())

    serialized = pickle.dumps(a)
    restored = pickle.loads(serialized)
    print("pickle restored same instance:", restored is a, id(restored) == id(a))

    copied = copy.copy(a)
    deepcopied = copy.deepcopy(a)
    print("copy is same instance:", copied is a)
    print("deepcopy is same instance:", deepcopied is a)