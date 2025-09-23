import threading
import pickle

class ApplicationConfig:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(ApplicationConfig, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.initialized = True
            self._data = {'version': '1.0', 'debug': True}
            self._access_count = 0
            self._lock_data = threading.Lock()

    def __reduce__(self):
        return (ApplicationConfig, ())

    def get_setting(self, key):
        with self._lock_data:
            self._access_count += 1
            return self._data.get(key, None)

    def set_setting(self, key, value):
        with self._lock_data:
            self._data[key] = value
            self._access_count += 1

    def get_access_count(self):
        with self._lock_data:
            return self._access_count

if __name__ == "__main__":
    def config_worker():
        config = ApplicationConfig()
        print(f"Worker accessing debug: {config.get_setting('debug')}")
        config.set_setting('temp', f'worker_{threading.current_thread().name}')
        print(f"Worker access count: {config.get_access_count()}")

    threads = []
    for i in range(3):
        t = threading.Thread(target=config_worker, name=f'T{i}')
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    config1 = ApplicationConfig()
    config1.set_setting('user', 'admin')
    print(f"Config1 debug: {config1.get_setting('debug')}")
    print(f"Config1 user: {config1.get_setting('user')}")
    print(f"Config1 access count: {config1.get_access_count()}")

    config2 = ApplicationConfig()
    print(f"Config2 user: {config2.get_setting('user')}")
    print(f"Config2 access count: {config2.get_access_count()}")
    print(f"Same instance: {config1 is config2}")

    pickled = pickle.dumps(config1)
    config3 = pickle.loads(pickled)
    print(f"Config3 user: {config3.get_setting('user')}")
    print(f"Config3 same as config1: {config3 is config1}")
    print(f"Final access count: {config3.get_access_count()}")