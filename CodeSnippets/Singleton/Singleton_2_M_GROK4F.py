class ConfigManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConfigManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._initialized = True
            self.config = {'host': 'localhost', 'port': 8080}

    def get_setting(self, key):
        if key in self.config:
            return self.config[key]
        raise ValueError(f"Setting '{key}' not found in configuration.")

    def update_setting(self, key, value):
        if not isinstance(key, str) or not key:
            raise ValueError("Key must be a non-empty string.")
        self.config[key] = value

if __name__ == '__main__':
    manager1 = ConfigManager()
    print(f"Host: {manager1.get_setting('host')}")
    print(f"Initial port: {manager1.get_setting('port')}")

    manager2 = ConfigManager()
    print(f"Same instance: {manager1 is manager2}")

    manager2.update_setting('port', 9090)
    print(f"Updated port: {manager1.get_setting('port')}")

    try:
        manager1.get_setting('invalid')
    except ValueError as e:
        print(f"Error: {e}")