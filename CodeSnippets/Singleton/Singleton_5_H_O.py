import threading
import pickle
import copy

def _unpickle_helper(cls, state):
    inst = cls()
    inst.__setstate__(state)
    return inst

class UniqueMeta(type):
    _instances = {}
    _locks = {}
    _meta_lock = threading.RLock()

    def __call__(cls, *args, **kwargs):
        meta = cls.__class__
        if cls in meta._instances:
            return meta._instances[cls]
        with meta._meta_lock:
            if cls not in meta._locks:
                meta._locks[cls] = threading.RLock()
            lock = meta._locks[cls]
        with lock:
            if cls in meta._instances:
                return meta._instances[cls]
            inst = super().__call__(*args, **kwargs)
            meta._instances[cls] = inst
            return inst

    def reset(cls):
        meta = cls.__class__
        with meta._meta_lock:
            if cls not in meta._locks:
                meta._locks[cls] = threading.RLock()
            lock = meta._locks[cls]
        with lock:
            meta._instances.pop(cls, None)

class GlobalResource(metaclass=UniqueMeta):
    def __init__(self, config=None):
        if getattr(self, "_initialized", False):
            return
        self._state_lock = threading.RLock()
        self.config = config
        self._initialized = True

    def perform(self, value):
        with self._state_lock:
            return (self.config, value)

    def __getstate__(self):
        state = self.__dict__.copy()
        state.pop("_state_lock", None)
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        if "_state_lock" not in self.__dict__ or not isinstance(self.__dict__.get("_state_lock"), threading.RLock):
            self._state_lock = threading.RLock()
        if "_initialized" not in self.__dict__:
            self._initialized = True

    def __reduce__(self):
        return (_unpickle_helper, (self.__class__, self.__getstate__()))

    def __copy__(self):
        return self

    def __deepcopy__(self, memo):
        return self

if __name__ == "__main__":
    a = GlobalResource({"mode": "first"})
    b = GlobalResource({"mode": "second"})
    print("a is b:", a is b)
    print("a.config:", a.config)
    GlobalResource.reset()
    c = GlobalResource({"mode": "after_reset"})
    print("a is c after reset:", a is c)
    print("c.config:", c.config)
    data = pickle.dumps(c)
    d = pickle.loads(data)
    print("d is c after pickle:", d is c)
    e = copy.copy(d)
    f = copy.deepcopy(d)
    print("copy is same:", e is d, "deepcopy is same:", f is d)