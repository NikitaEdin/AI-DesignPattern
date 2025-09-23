import threading
import pickle
import copy

class SingleInstanceMeta(type):
    _instances = {}
    _lock = threading.RLock()

    def __call__(cls, *args, **kwargs):
        with SingleInstanceMeta._lock:
            if cls in SingleInstanceMeta._instances:
                return SingleInstanceMeta._instances[cls]
            instance = super().__call__(*args, **kwargs)
            SingleInstanceMeta._instances[cls] = instance
            return instance

def get_unique_instance(cls):
    inst = SingleInstanceMeta._instances.get(cls)
    if inst is not None:
        return inst
    return cls()

class UniqueBase(metaclass=SingleInstanceMeta):
    def __new__(cls, *args, **kwargs):
        inst = type(cls)._instances.get(cls)
        if inst is not None:
            return inst
        return super().__new__(cls)

    def __reduce__(self):
        return (get_unique_instance, (self.__class__,), self.__dict__)

    def __copy__(self):
        return self

    def __deepcopy__(self, memo):
        return self

class ConfigManager(UniqueBase):
    def __init__(self, config=None):
        if not getattr(self, "_initialized", False):
            self._initialized = True
            self.config = dict(config) if config else {}

    def set_value(self, key, value):
        self.config[key] = value

    def get_value(self, key, default=None):
        return self.config.get(key, default)

if __name__ == "__main__":
    mgr1 = ConfigManager({"a": 1})
    mgr2 = ConfigManager()
    mgr2.set_value("b", 2)

    print("mgr1 is mgr2:", mgr1 is mgr2)
    print("mgr1 config:", mgr1.config)
    print("mgr2 config:", mgr2.config)

    def create_instance(container, index):
        container[index] = ConfigManager()

    threads = []
    results = [None] * 10
    for i in range(10):
        t = threading.Thread(target=create_instance, args=(results, i))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()

    ids = {id(obj) for obj in results}
    print("Unique instance across threads:", len(ids) == 1)

    copied = copy.copy(mgr1)
    deepcopied = copy.deepcopy(mgr1)
    print("copy is original:", copied is mgr1)
    print("deepcopy is original:", deepcopied is mgr1)

    data = pickle.dumps(mgr1)
    restored = pickle.loads(data)
    print("restored is original:", restored is mgr1)