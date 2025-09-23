class ConfigurationManager:
    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._initialized:
            self.settings = {}
            self._initialized = True

    def set(self, key, value):
        if not isinstance(key, str):
            raise TypeError("Key must be a string")
        self.settings[key] = value

    def get(self, key, default=None):
        return self.settings.get(key, default)

    def clear(self):
        self.settings.clear()


if __name__ == "__main__":
    manager1 = ConfigurationManager()
    manager2 = ConfigurationManager()
    
    manager1.set("debug", True)
    manager1.set("port", 8080)
    
    manager2.set("host", "localhost")
    
    print(manager1 is manager2)
    print(manager1.get("debug"))
    print(manager2.get("port"))
    print(manager2.get("host"))