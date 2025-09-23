class Configuration:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'value'):
            self.value = "default config"

if __name__ == "__main__":
    config1 = Configuration()
    config2 = Configuration()
    print(config1.value)
    print(config2.value)
    print(config1 is config2)