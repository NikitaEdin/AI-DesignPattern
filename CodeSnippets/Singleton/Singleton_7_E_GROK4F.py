class ConfigManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConfigManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.initialized = True
            self.setting = "default_value"

if __name__ == "__main__":
    instance1 = ConfigManager()
    instance2 = ConfigManager()
    print(instance1 is instance2)
    print(instance1.setting)