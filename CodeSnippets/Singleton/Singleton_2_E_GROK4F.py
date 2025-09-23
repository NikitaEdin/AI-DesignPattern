class AppConfig:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AppConfig, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, '_initialized'):
            self.value = "default"
            self._initialized = True

if __name__ == "__main__":
    config1 = AppConfig()
    config1.value = "updated"
    config2 = AppConfig()
    print(config1 is config2)
    print(config2.value)