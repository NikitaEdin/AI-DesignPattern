import threading


class OneInstanceMeta(type):
    _instances = {}
    _lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            with cls._lock:
                if cls not in cls._instances:
                    instance = super().__call__(*args, **kwargs)
                    cls._instances[cls] = instance
        return cls._instances[cls]


class ConfigManager(metaclass=OneInstanceMeta):
    def __init__(self, initial_values=None):
        if getattr(self, "_initialized", False):
            return
        self._store = dict(initial_values or {})
        self._store_lock = threading.RLock()
        self._initialized = True

    def set_option(self, key, value):
        if not isinstance(key, str):
            raise TypeError("Key must be a string")
        with self._store_lock:
            self._store[key] = value

    def get_option(self, key, default=None):
        if not isinstance(key, str):
            raise TypeError("Key must be a string")
        with self._store_lock:
            return self._store.get(key, default)

    def load_from_dict(self, data):
        if not isinstance(data, dict):
            raise TypeError("Data must be a dictionary")
        with self._store_lock:
            for k, v in data.items():
                if not isinstance(k, str):
                    raise TypeError("All keys must be strings")
            self._store.update(data)

    def export(self):
        with self._store_lock:
            return dict(self._store)


if __name__ == "__main__":
    manager_a = ConfigManager({"mode": "production", "timeout": 30})
    manager_b = ConfigManager()

    print("manager_a id:", id(manager_a))
    print("manager_b id:", id(manager_b))
    print("Same object:", manager_a is manager_b)

    print("Initial mode:", manager_b.get_option("mode"))

    manager_a.set_option("mode", "debug")
    print("Updated mode via manager_a:", manager_b.get_option("mode"))

    try:
        manager_b.set_option(123, "invalid")
    except TypeError as err:
        print("Error caught:", err)

    manager_a.load_from_dict({"retries": 5})
    print("Exported configuration:", manager_b.export())