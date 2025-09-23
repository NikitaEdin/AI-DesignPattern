import threading
import pickle
import copy

class UniqueMeta(type):
    _instances = {}
    _locks = {}
    def __call__(cls, *args, **kwargs):
        if cls in UniqueMeta._instances:
            return UniqueMeta._instances[cls]
        lock = UniqueMeta._locks.setdefault(cls, threading.RLock())
        with lock:
            if cls in UniqueMeta._instances:
                return UniqueMeta._instances[cls]
            inst = super().__call__(*args, **kwargs)
            UniqueMeta._instances[cls] = inst
            return inst
    def get_instance(cls):
        return cls()
    def _reset_instance(cls):
        lock = UniqueMeta._locks.setdefault(cls, threading.RLock())
        with lock:
            UniqueMeta._instances.pop(cls, None)

class GlobalResource(metaclass=UniqueMeta):
    def __init__(self, name="default", **settings):
        self.name = name
        self.settings = dict(settings)
        self._initialized = True
    def update(self, **kwargs):
        self.settings.update(kwargs)
    def info(self):
        return {"name": self.name, "settings": dict(self.settings)}
    def __copy__(self):
        return self
    def __deepcopy__(self, memo):
        return self
    def __reduce__(self):
        return (self.__class__.get_instance, ())

def _thread_target(results, index, name):
    r = GlobalResource(name=name, version=index)
    results[index] = id(r)

if __name__ == "__main__":
    # single-threaded creation and reuse
    a = GlobalResource(name="primary", host="localhost")
    b = GlobalResource(name="secondary", host="remote")
    assert id(a) == id(b)
    assert a.info()["name"] == "primary"
    a.update(port=8080)
    assert b.info()["settings"]["port"] == 8080

    # thread-safe creation demonstration
    threads = []
    results = [None] * 8
    for i in range(8):
        t = threading.Thread(target=_thread_target, args=(results, i, f"node{i}"))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    assert len(set(results)) == 1

    # copying and pickling preserve the same instance
    c = copy.copy(a)
    d = copy.deepcopy(a)
    e = pickle.loads(pickle.dumps(a))
    assert id(a) == id(c) == id(d) == id(e)

    # reset for testing and recreate with new parameters
    GlobalResource._reset_instance()
    f = GlobalResource(name="recreated", host="newhost")
    assert id(f) != id(a)
    print("All checks passed. Instance id:", id(f))