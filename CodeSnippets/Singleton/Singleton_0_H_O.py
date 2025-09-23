import threading
import copy
import pickle

class SingleInstanceMeta(type):
    _instances = {}
    _lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        if cls not in SingleInstanceMeta._instances:
            with SingleInstanceMeta._lock:
                if cls not in SingleInstanceMeta._instances:
                    instance = cls.__new__(cls, *args, **kwargs)
                    cls.__init__(instance, *args, **kwargs)
                    SingleInstanceMeta._instances[cls] = instance
        return SingleInstanceMeta._instances[cls]

class BaseSingle(metaclass=SingleInstanceMeta):
    def __reduce__(self):
        return (self.__class__, (), self.__dict__)

    def __copy__(self):
        return self

    def __deepcopy__(self, memo):
        return self

    @classmethod
    def release_instance(cls):
        with SingleInstanceMeta._lock:
            SingleInstanceMeta._instances.pop(cls, None)

class AppCore(BaseSingle):
    def __init__(self, initial=0):
        if getattr(self, '_initialized', False):
            return
        self.counter = int(initial)
        self._initialized = True
        self._lock = threading.Lock()

    def increment(self, step=1):
        with self._lock:
            self.counter += int(step)
            return self.counter

    def get_state(self):
        return {'counter': self.counter}

if __name__ == "__main__":
    def worker(start_value, results, index):
        obj = AppCore(start_value)
        obj.increment()
        results[index] = obj

    threads = []
    results = [None] * 8
    for i in range(8):
        t = threading.Thread(target=worker, args=(i, results, i))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()

    ids = [id(r) for r in results]
    same = all(i == ids[0] for i in ids)
    print("All instances same object:", same)
    print("Instance id:", ids[0])
    print("Shared state after threaded increments:", results[0].get_state())

    serialized = pickle.dumps(AppCore())
    deserialized = pickle.loads(serialized)
    print("Pickle preserved identity:", deserialized is AppCore())

    cpy = copy.copy(deserialized)
    dcpy = copy.deepcopy(deserialized)
    print("Copy preserved identity:", cpy is deserialized)
    print("Deepcopy preserved identity:", dcpy is deserialized)

    AppCore.release_instance()
    fresh = AppCore(42)
    print("New instance after release:", fresh.get_state())