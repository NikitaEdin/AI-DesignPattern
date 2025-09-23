import threading
import concurrent.futures
import copy

class OnlyOneMeta(type):
    _instances = {}
    _locks = {}
    _global_lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        if cls not in OnlyOneMeta._locks:
            with OnlyOneMeta._global_lock:
                if cls not in OnlyOneMeta._locks:
                    OnlyOneMeta._locks[cls] = threading.RLock()
        lock = OnlyOneMeta._locks[cls]
        with lock:
            if cls not in OnlyOneMeta._instances:
                instance = super().__call__(*args, **kwargs)
                OnlyOneMeta._instances[cls] = instance
            return OnlyOneMeta._instances[cls]

class UniqueBase(metaclass=OnlyOneMeta):
    def __copy__(self):
        return self

    def __deepcopy__(self, memo):
        return self

    def __reduce__(self):
        return (self.__class__, ())

    @classmethod
    def release_single(cls):
        lock = OnlyOneMeta._locks.get(cls)
        if lock:
            with lock:
                OnlyOneMeta._instances.pop(cls, None)

class ResourceManager(UniqueBase):
    def __init__(self, value=0):
        if getattr(self, "_initialized", False):
            return
        self.value = value
        self._initialized = True

    def increment(self, amount=1):
        self.value += amount
        return self.value

    @classmethod
    def current_identity(cls):
        instance = cls()
        return id(instance)

def _create_resource(arg):
    inst = ResourceManager(arg)
    return id(inst), inst.value

if __name__ == "__main__":
    a = ResourceManager(10)
    b = ResourceManager(20)
    print("a is b:", a is b)
    print("a.value:", a.value)
    print("b.value:", b.value)

    ids = set()
    values = set()
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
        futures = [ex.submit(_create_resource, i) for i in range(8)]
        for fut in concurrent.futures.as_completed(futures):
            inst_id, val = fut.result()
            ids.add(inst_id)
            values.add(val)
    print("unique ids from threads:", ids)
    print("values observed from threads:", values)

    ResourceManager.release_single()
    c = ResourceManager(99)
    print("After release, new instance created:", id(c), c.value)

    d = copy.copy(c)
    e = copy.deepcopy(c)
    print("copy id equals:", id(d) == id(c))
    print("deepcopy id equals:", id(e) == id(c))