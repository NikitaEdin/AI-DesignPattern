class AppConfig:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        self.database_url = "sqlite:///app.db"
        self.debug_mode = False
        self.max_connections = 100
        self._initialized = True
    
    def configure(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                raise ValueError(f"Unknown configuration parameter: {key}")
    
    def get_config(self):
        return {
            'database_url': self.database_url,
            'debug_mode': self.debug_mode,
            'max_connections': self.max_connections
        }

if __name__ == "__main__":
    config1 = AppConfig()
    config2 = AppConfig()
    
    print(f"Same instance: {config1 is config2}")
    
    config1.configure(debug_mode=True, max_connections=50)
    
    print(f"Config from instance 1: {config1.get_config()}")
    print(f"Config from instance 2: {config2.get_config()}")
    
    try:
        config1.configure(unknown_setting="value")
    except ValueError as e:
        print(f"Error: {e}")