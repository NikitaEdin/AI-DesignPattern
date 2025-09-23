class ConfigManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(ConfigManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self.settings = {}
        self._initialized = True

    def set_value(self, key, value):
        self.settings[key] = value

    def get_value(self, key, default=None):
        return self.settings.get(key, default)


if __name__ == "__main__":
    a = ConfigManager()
    b = ConfigManager()
    a.set_value("mode", "production")
    print(a is b)
    print(id(a), id(b))
    print(b.get_value("mode"))