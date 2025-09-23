import threading
import time
import pickle

class InstanceKeeperMeta(type):
    _instances = {}
    _lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        if cls not in InstanceKeeperMeta._instances:
            with InstanceKeeperMeta._lock:
                if cls not in InstanceKeeperMeta._instances:
                    InstanceKeeperMeta._instances[cls] = super().__call__(*args, **kwargs)
        return InstanceKeeperMeta._instances[cls]

class GlobalResource(metaclass=InstanceKeeperMeta):
    def __init__(self, config=None):
        if getattr(self, "_initialized", False):
            return
        self.config = config
        self.created_at = time.time()
        self._initialized = True

    def __reduce__(self):
        return (self.__class__, (self.config,))

    def info(self):
        return {"config": self.config, "created_at": self.created_at}

if __name__ == "__main__":
    a = GlobalResource("initial")
    b = GlobalResource("override")
    print(a is b)
    print(a.config)
    print(b.config)

    serialized = pickle.dumps(a)
    restored = pickle.loads(serialized)
    print(restored is a)

    results = []
    def worker(i):
        inst = GlobalResource(f"from-{i}")
        results.append(id(inst))

    threads = [threading.Thread(target=worker, args=(i,)) for i in range(8)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    print(len(set(results)) == 1)
    print(a.info())