import threading


class AppConfig:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self, config_file="config.json"):
        if self._initialized:
            return
        self.config_file = config_file
        self.settings = {}
        self._load()
        self._initialized = True

    def _load(self):
        try:
            with open(self.config_file, "r") as f:
                import json
                self.settings = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.settings = {"default": True}

    def get(self, key, default=None):
        return self.settings.get(key, default)

    def set(self, key, value):
        self.settings[key] = value


if __name__ == "__main__":
    config1 = AppConfig("app.json")
    config2 = AppConfig("ignored.json")

    config1.set("theme", "dark")
    print(config2.get("theme"))

    print(config1 is config2)