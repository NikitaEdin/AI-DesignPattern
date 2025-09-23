import threading


class ConfigManager:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance.config = {}
        return cls._instance

    def set(self, key, value):
        self.config[key] = value

    def get(self, key):
        return self.config.get(key)


if __name__ == "__main__":
    a = ConfigManager()
    b = ConfigManager()

    a.set("debug", True)
    print(b.get("debug"))  # True

    print(a is b)  # True