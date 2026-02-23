import threading
import time

class UniqueManagerMeta(type):
    _instances = {}
    _lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]

class ResourceManager(metaclass=UniqueManagerMeta):
    def __init__(self, config=None):
        if not hasattr(self, '_initialized'):
            self._initialized = True
            self.config = config if config is not None else {}
            self.access_count = 0

    def get_config(self):
        self.access_count += 1
        return self.config.copy()

    def update_config(self, key, value):
        self.access_count += 1
        self.config[key] = value

    def get_access_count(self):
        return self.access_count

    def __reduce__(self):
        return (self.__class__, ())

def threaded_creation(results, index):
    time.sleep(0.01)  # Simulate some delay
    rm = ResourceManager()
    results[index] = rm

if __name__ == "__main__":
    # Basic usage
    rm1 = ResourceManager({'initial': 'value'})
    rm2 = ResourceManager({'different': 'value'})  # Should not change the config

    print("Are rm1 and rm2 the same instance?", rm1 is rm2)
    print("Config from rm1:", rm1.get_config())
    print("Config from rm2:", rm2.get_config())

    # Update config from rm1
    rm1.update_config('new_key', 'new_value')
    print("Config after update from rm1:", rm2.get_config())
    print("Access count from rm1:", rm1.get_access_count())
    print("Access count from rm2:", rm2.get_access_count())

    # Threading test
    results = [None] * 5
    threads = []
    for i in range(5):
        t = threading.Thread(target=threaded_creation, args=(results, i))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    all_same = all(r is results[0] for r in results)
    print("All instances from threads are the same?", all_same)
    print("Final config:", results[0].get_config())
    print("Final access count:", results[0].get_access_count())

    # Serialization test
    import pickle
    pickled = pickle.dumps(rm1)
    unpickled = pickle.loads(pickled)
    print("Unpickled is same instance?", unpickled is rm1)
    print("Unpickled config:", unpickled.get_config())
    print("Unpickled access count:", unpickled.get_access_count())