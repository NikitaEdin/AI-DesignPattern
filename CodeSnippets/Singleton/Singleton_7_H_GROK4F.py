import threading
import pickle
import os

class ConfigurationManager:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(ConfigurationManager, cls).__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._config = {}
        self._initialized = True
        self._load_default_config()

    def _load_default_config(self):
        self._config['debug'] = os.environ.get('DEBUG', 'False').lower() == 'true'
        self._config['timeout'] = int(os.environ.get('TIMEOUT', '30'))

    @classmethod
    def get_instance(cls):
        return cls()

    def get(self, key, default=None):
        return self._config.get(key, default)

    def set(self, key, value):
        self._config[key] = value

    def __getstate__(self):
        state = self._config.copy()
        state['_instance_id'] = id(self)
        return state

    def __setstate__(self, state):
        self._config = state.copy()
        self._initialized = True
        if '_instance_id' in state:
            del self._config['_instance_id']

    def __reduce__(self):
        return (ConfigurationManager.get_instance, ())

    def __deepcopy__(self, memo):
        return self

    def validate_config(self):
        required_keys = ['debug', 'timeout']
        missing = [k for k in required_keys if k not in self._config]
        if missing:
            raise ValueError(f"Missing required config keys: {missing}")
        if not isinstance(self._config['timeout'], int) or self._config['timeout'] <= 0:
            raise ValueError("Timeout must be a positive integer")

def worker_thread():
    mgr1 = ConfigurationManager.get_instance()
    mgr1.set('thread_id', threading.current_thread().name)
    return id(mgr1)

def demonstrate_usage():
    print("Direct instantiation:")
    mgr_a = ConfigurationManager()
    print(f"ID of first instance: {id(mgr_a)}")
    print(f"Debug mode: {mgr_a.get('debug')}")

    mgr_b = ConfigurationManager()
    print(f"ID of second instance: {id(mgr_b)}")
    assert id(mgr_a) == id(mgr_b), "Instances should be the same"

    mgr_b.set('custom_key', 'value')
    print(f"Value from second instance: {mgr_a.get('custom_key')}")

    print("\nThread safety demonstration:")
    threads = []
    for i in range(5):
        t = threading.Thread(target=worker_thread, name=f"Thread-{i}")
        threads.append(t)
        t.start()
    for t in threads:
        t.join()

    print("\nPickling demonstration:")
    mgr_c = ConfigurationManager.get_instance()
    mgr_c.set('pickled_key', 'persistent_value')
    pickled = pickle.dumps(mgr_c)
    mgr_d = pickle.loads(pickled)
    print(f"ID before pickling: {id(mgr_c)}")
    print(f"ID after unpickling: {id(mgr_d)}")
    assert id(mgr_c) == id(mgr_d), "Pickled instances should be the same"
    print(f"Retrieved pickled value: {mgr_d.get('pickled_key')}")

    print("\nEdge case: Validation")
    try:
        ConfigurationManager().validate_config()
        print("Config validation passed")
    except ValueError as e:
        print(f"Validation error (expected if invalid): {e}")

    print("\nReset for testing (advanced feature):")
    ConfigurationManager._instance = None
    ConfigurationManager._lock = threading.Lock()  # Reset lock
    mgr_reset = ConfigurationManager.get_instance()
    print(f"New instance ID after reset: {id(mgr_reset)}")

if __name__ == "__main__":
    demonstrate_usage()