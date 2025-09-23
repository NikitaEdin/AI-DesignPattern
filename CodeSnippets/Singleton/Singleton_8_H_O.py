import threading
import pickle
import copy

def _get_existing(cls):
    return cls()

class UniqueEnforcerMeta(type):
    _instances = {}
    _locks = {}

    def __call__(cls, *args, **kwargs):
        if cls in UniqueEnforcerMeta._instances:
            existing = UniqueEnforcerMeta._instances[cls]
            sig = getattr(existing, "_init_signature", None)
            if sig is not None and sig != (args, kwargs):
                raise TypeError("Instance already created with different initialization arguments")
            return existing
        lock = UniqueEnforcerMeta._locks.setdefault(cls, threading.Lock())
        with lock:
            if cls in UniqueEnforcerMeta._instances:
                return UniqueEnforcerMeta._instances[cls]
            inst = super().__call__(*args, **kwargs)
            setattr(inst, "_init_signature", (args, kwargs))
            UniqueEnforcerMeta._instances[cls] = inst
            return inst

    def reset(cls):
        lock = UniqueEnforcerMeta._locks.setdefault(cls, threading.Lock())
        with lock:
            inst = UniqueEnforcerMeta._instances.pop(cls, None)
            if inst and hasattr(inst, "_init_signature"):
                try:
                    delattr(inst, "_init_signature")
                except Exception:
                    pass
            return inst

class GlobalResource(metaclass=UniqueEnforcerMeta):
    def __init__(self, name="resource", config=None):
        self.name = name
        self.config = dict(config or {})
        self._counter = 0
        self._lock = threading.Lock()

    def increment(self):
        with self._lock:
            self._counter += 1
            return self._counter

    def get_state(self):
        return {"name": self.name, "config": dict(self.config), "count": self._counter}

    def __repr__(self):
        return f"<GlobalResource name={self.name!r} id={id(self)}>"

    def __copy__(self):
        return self

    def __deepcopy__(self, memo):
        return self

    def __reduce__(self):
        return (_get_existing, (self.__class__,))

if __name__ == "__main__":
    created_ids = []
    def worker(index, results):
        inst = GlobalResource("app", {"mode": "prod"})
        inst.increment()
        results.append(id(inst))

    threads = []
    results = []
    for i in range(8):
        t = threading.Thread(target=worker, args=(i, results))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()

    print("All ids equal:", all(x == results[0] for x in results), "id:", results[0])

    a = GlobalResource("app", {"mode": "prod"})
    b = GlobalResource()
    print("Same object via direct calls:", a is b)

    data = pickle.dumps(a)
    c = pickle.loads(data)
    print("Pickle preserves identity:", c is a)

    d = copy.copy(a)
    e = copy.deepcopy(a)
    print("Copy preserved identity:", d is a, "Deepcopy preserved identity:", e is a)

    try:
        GlobalResource("other", {"mode": "test"})
    except TypeError as exc:
        print("Attempt to reinitialize with different args raised:", type(exc).__name__)

    GlobalResource.reset()
    new_inst = GlobalResource("other", {"mode": "test"})
    print("New instance after reset:", new_inst, "state:", new_inst.get_state())