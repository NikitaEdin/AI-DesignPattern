import threading

class ConfigManager:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._settings = {}
        return cls._instance

    def set(self, key, value):
        if not isinstance(key, str):
            raise TypeError("Key must be a string")
        self._settings[key] = value

    def get(self, key):
        return self._settings.get(key)

    def list_all(self):
        return dict(self._settings)

if __name__ == "__main__":
    manager1 = ConfigManager()
    manager1.set("debug", True)
    manager1.set("max_connections", 100)

    manager2 = ConfigManager()
    print(manager2.get("debug"))
    print(manager2 is manager1)
    print(manager2.list_all())