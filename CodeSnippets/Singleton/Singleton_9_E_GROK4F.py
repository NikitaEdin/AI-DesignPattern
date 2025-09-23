class ConfigurationManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.initialized = True
            self.settings = {}

if __name__ == "__main__":
    instance1 = ConfigurationManager()
    instance2 = ConfigurationManager()
    print(instance1 is instance2)
    print(id(instance1) == id(instance2))