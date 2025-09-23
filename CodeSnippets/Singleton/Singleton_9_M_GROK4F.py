import threading

class ConfigManager:
    _instance = None
    _lock = threading.RLock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._settings = {}
            self._initialized = True

    def get_setting(self, key, default=None):
        return self._settings.get(key, default)

    def set_setting(self, key, value):
        self._settings[key] = value

    def load_from_dict(self, data):
        self._settings.update(data)

if __name__ == "__main__":
    cm1 = ConfigManager()
    cm1.set_setting('key1', 'value1')
    print(f"Instance 1 ID: {id(cm1)}, Setting: {cm1.get_setting('key1')}")

    cm2 = ConfigManager()
    cm2.set_setting('key2', 'value2')
    print(f"Instance 2 ID: {id(cm2)}, Setting key1: {cm2.get_setting('key1')}, key2: {cm2.get_setting('key2')}")

    # Demonstrate shared state
    print(f"Shared instance confirmed: {cm1 is cm2}")