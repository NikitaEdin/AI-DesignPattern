class ApplicationConfig:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.initialized = True
            self.setting = "default_value"

if __name__ == "__main__":
    config1 = ApplicationConfig()
    config2 = ApplicationConfig()
    print(config1 is config2)
    print(config1.setting)
    print(config2.setting)