class ConfigurationManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.value = "Initialized"
        return cls._instance

if __name__ == "__main__":
    config1 = ConfigurationManager()
    config2 = ConfigurationManager()
    print(config1 is config2)
    print(config1.value)
    config2.value = "Updated"
    print(config1.value)