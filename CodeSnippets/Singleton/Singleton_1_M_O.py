import threading
import time

class InstanceControlMeta(type):
    _instances = {}
    _global_lock = threading.RLock()

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            with InstanceControlMeta._global_lock:
                if cls not in cls._instances:
                    instance = super().__call__(*args, **kwargs)
                    InstanceControlMeta._instances[cls] = instance
        return InstanceControlMeta._instances[cls]

class AppConfig(metaclass=InstanceControlMeta):
    def __init__(self, initial=None):
        if getattr(self, "_initialized", False):
            return
        self._lock = threading.RLock()
        if initial is None:
            self._data = {}
        elif isinstance(initial, dict):
            self._data = dict(initial)
        else:
            raise TypeError("initial configuration must be a dict or None")
        self._initialized = True

    def get(self, key, default=None):
        with self._lock:
            return self._data.get(key, default)

    def set(self, key, value):
        if not isinstance(key, str):
            raise TypeError("key must be a string")
        with self._lock:
            self._data[key] = value

    def update(self, mapping):
        if not isinstance(mapping, dict):
            raise TypeError("mapping must be a dict")
        with self._lock:
            self._data.update(mapping)

    def to_dict(self):
        with self._lock:
            return dict(self._data)

def _create_instance_in_thread(results, index, initial):
    try:
        cfg = AppConfig(initial)
        results[index] = id(cfg)
    except Exception as e:
        results[index] = f"error:{e}"

if __name__ == "__main__":
    cfg1 = AppConfig({"mode": "initial", "retries": 3})
    cfg2 = AppConfig()
    print("cfg1 id:", id(cfg1))
    print("cfg2 id:", id(cfg2))
    print("same instance:", id(cfg1) == id(cfg2))
    print("initial data:", cfg1.to_dict())

    cfg2.set("mode", "updated")
    cfg2.set("timeout", 30)
    print("after update via cfg2, cfg1 data:", cfg1.to_dict())

    try:
        cfg1.update({"retries": 5, "verbose": True})
    except TypeError as e:
        print("update error:", e)
    print("after update:", cfg1.to_dict())

    thread_count = 6
    threads = []
    results = [None] * thread_count
    for i in range(thread_count):
        t = threading.Thread(target=_create_instance_in_thread, args=(results, i, {"thread": i}))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()

    print("thread results ids:", results)
    unique_ids = set(x for x in results if isinstance(x, int))
    print("unique ids from threads:", unique_ids)
    print("single instance across threads:", len(unique_ids) == 1)