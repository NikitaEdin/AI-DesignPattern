class ConfigManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.initialized = True
            self.settings = {}

    def set_setting(self, key, value):
        self.settings[key] = value
    
    def get_setting(self, key):
        return self.settings.get(key)

if __name__ == "__main__":
    config1 = ConfigManager()
    config2 = ConfigManager()
    
    config1.set_setting("theme", "dark")
    
    print(config2.get_setting("theme"))  # Output: dark
    print(config1 is config2)  # Output: True