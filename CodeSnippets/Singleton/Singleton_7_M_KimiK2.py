class AppConfig:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self.settings = {}
        self._initialized = True

    def set(self, key, value):
        self.settings[key] = value

    def get(self, key, default=None):
        return self.settings.get(key, default)


if __name__ == "__main__":
    c1 = AppConfig()
    c1.set("theme", "dark")
    c2 = AppConfig()
    c2.set("language", "en")
    print(c1 is c2)
    print(c1.get("theme"), c2.get("language"))
    print(c1.get("language"), c2.get("theme"))