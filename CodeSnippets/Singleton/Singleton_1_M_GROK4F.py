class AppConfig:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AppConfig, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._config = {}
            self._initialized = True

    def set_value(self, key, value):
        if not isinstance(key, str):
            raise ValueError("Key must be a string")
        self._config[key] = value

    def get_value(self, key):
        if not isinstance(key, str):
            raise ValueError("Key must be a string")
        return self._config.get(key, None)

    def clear(self):
        self._config.clear()

if __name__ == "__main__":
    config1 = AppConfig()
    config1.set_value("database_url", "sqlite:///app.db")
    config1.set_value("debug_mode", True)

    config2 = AppConfig()
    value1 = config2.get_value("database_url")
    value2 = config2.get_value("debug_mode")

    print(f"Database URL: {value1}")
    print(f"Debug Mode: {value2}")
    print(f"Same instance: {config1 is config2}")

    config2.set_value("api_key", "secret123")
    print(f"API Key from config1: {config1.get_value('api_key')}")