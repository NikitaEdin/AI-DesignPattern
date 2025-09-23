import threading
import weakref
import copy
import pickle

class OnlyOneMeta(type):
    _instances = weakref.WeakValueDictionary()
    _locks = {}
    _global_lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        meta = type(cls)
        inst = meta._instances.get(cls)
        if inst is not None:
            return inst
        with meta._global_lock:
            lock = meta._locks.get(cls)
            if lock is None:
                lock = threading.Lock()
                meta._locks[cls] = lock
        with lock:
            inst = meta._instances.get(cls)
            if inst is None:
                inst = super().__call__(*args, **kwargs)
                meta._instances[cls] = inst
        return inst

    @classmethod
    def reset_for(mcls, target_cls):
        with mcls._global_lock:
            lock = mcls._locks.get(target_cls)
            if lock is None:
                lock = threading.Lock()
                mcls._locks[target_cls] = lock
        with lock:
            mcls._instances.pop(target_cls, None)

class AppConfig(metaclass=OnlyOneMeta):
    def __init__(self, value=None):
        if getattr(self, "_initialized", False):
            return
        self.value = value
        self._initialized = True

    def __copy__(self):
        return self

    def __deepcopy__(self, memo):
        return self

    def __reduce__(self):
        state = self.__dict__.copy()
        return (self.__class__, (), state)

    def __setstate__(self, state):
        self.__dict__.update(state)

if __name__ == "__main__":
    a = AppConfig(1)
    b = AppConfig(2)
    print("a is b:", a is b)
    print("a.value:", a.value, "b.value:", b.value)

    import copy as _copy
    print("copy(a) is a:", _copy.copy(a) is a)

    data = pickle.dumps(a)
    restored = pickle.loads(data)
    print("restored is a:", restored is a)

    type(AppConfig).reset_for(AppConfig)
    c = AppConfig(3)
    print("a is c after reset:", a is c)
    print("c.value:", c.value)