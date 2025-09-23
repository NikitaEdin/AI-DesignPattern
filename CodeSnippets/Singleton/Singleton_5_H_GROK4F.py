import threading
import copy
import pickle

class InstanceController(type):
    _instances = {}
    _lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
            return cls._instances[cls]

class ResourceManager(metaclass=InstanceController):
    def __init__(self):
        self._data = {}
        self._counter = 0

    def get_data(self):
        self._counter += 1
        return self._data, self._counter

    def __copy__(self):
        return self

    def __deepcopy__(self, memo):
        return self

    def __reduce__(self):
        return (self.__class__, ())

def worker():
    mgr1 = ResourceManager()
    data1, count1 = mgr1.get_data()
    mgr2 = ResourceManager()
    data2, count2 = mgr2.get_data()
    print(f"Worker: same instance: {mgr1 is mgr2}, data: {data1 is data2}, count: {count2}")

if __name__ == "__main__":
    import threading

    threads = []
    for _ in range(3):
        t = threading.Thread(target=worker)
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    mgr_a = ResourceManager()
    mgr_b = ResourceManager()
    print(f"Direct: same instance: {mgr_a is mgr_b}")

    mgr_c = copy.copy(mgr_a)
    print(f"Copy: same instance: {mgr_a is mgr_c}")

    pickled = pickle.dumps(mgr_a)
    mgr_d = pickle.loads(pickled)
    print(f"Pickle: same instance: {mgr_a is mgr_d}")

    data_a, count_a = mgr_a.get_data()
    data_b, count_b = mgr_b.get_data()
    print(f"Shared data: {data_a is data_b}, shared count: {count_b}")