import threading
import weakref
from copy import copy, deepcopy
from threading import Lock

class UniqueInstanceMeta(type):
    _instances = weakref.WeakValueDictionary()
    _lock = Lock()

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            with cls._lock:
                if cls not in cls._instances:
                    instance = super().__call__(*args, **kwargs)
                    cls._instances[cls] = instance
        return cls._instances[cls]

class ResourceManager(metaclass=UniqueInstanceMeta):
    _config_lock = Lock()
    _initialized = False
    _config = None

    def __init__(self):
        if not ResourceManager._initialized:
            with ResourceManager._config_lock:
                if not ResourceManager._initialized:
                    self._config = {}
                    self._load_default_config()
                    ResourceManager._initialized = True

    def _load_default_config(self):
        self._config['database_url'] = 'sqlite:///default.db'
        self._config['max_connections'] = 10

    def get_config(self):
        if self._config is None:
            with ResourceManager._config_lock:
                if self._config is None:
                    self._config = {}
                    self._load_default_config()
        return self._config

    def update_config(self, key, value):
        with ResourceManager._config_lock:
            if self._config is not None:
                self._config[key] = value
            else:
                raise RuntimeError("Configuration not initialized")

    def __copy__(self):
        raise TypeError("ResourceManager instances cannot be copied")

    def __deepcopy__(self, memo):
        raise TypeError("ResourceManager instances cannot be deep-copied")

def worker_thread(tid):
    rm = ResourceManager()
    config = rm.get_config()
    rm.update_config(f'thread_{tid}', tid)
    print(f"Thread {tid}: Config updated, instance id: {id(rm)}")

if __name__ == "__main__":
    print("Single-threaded test:")
    rm1 = ResourceManager()
    rm2 = ResourceManager()
    print(f"Instances same: {rm1 is rm2}")
    print(f"Config: {rm1.get_config()}")

    print("\nMulti-threaded test:")
    threads = []
    for i in range(5):
        t = threading.Thread(target=worker_thread, args=(i,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    final_rm = ResourceManager()
    print(f"Final instance id: {id(final_rm)}")
    print(f"Final config: {final_rm.get_config()}")