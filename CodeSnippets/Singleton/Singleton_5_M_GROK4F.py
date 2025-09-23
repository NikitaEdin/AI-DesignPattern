class ApplicationConfig:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ApplicationConfig, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.initialized = True
            self.settings = {
                'host': 'localhost',
                'port': 8080,
                'debug': False
            }

    def get_setting(self, key):
        if key in self.settings:
            return self.settings[key]
        raise ValueError(f"Setting '{key}' not found.")

    def set_setting(self, key, value):
        if not isinstance(key, str) or not key:
            raise ValueError("Key must be a non-empty string.")
        self.settings[key] = value

if __name__ == "__main__":
    config1 = ApplicationConfig()
    config2 = ApplicationConfig()

    print(config1 is config2)

    print(config1.get_setting('host'))
    print(config1.get_setting('port'))

    config1.set_setting('debug', True)
    print(config2.get_setting('debug'))

    config2.set_setting('timeout', 30)
    print(config1.get_setting('timeout'))

    try:
        config1.get_setting('invalid_key')
    except ValueError as e:
        print(e)

    try:
        config2.set_setting('', 'value')
    except ValueError as e:
        print(e)