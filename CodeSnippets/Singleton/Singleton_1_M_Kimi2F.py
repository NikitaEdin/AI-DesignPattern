import threading

class AppConfig:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self.db_url = "sqlite:///app.db"
        self.debug = False
        self.retries = 3
        self._initialized = True

    def reload_from_env(self):
        import os
        self.db_url = os.getenv("DB_URL", self.db_url)
        self.debug = os.getenv("DEBUG", "").lower() in {"1", "true", "yes"}
        self.retries = int(os.getenv("RETRIES", self.retries))

if __name__ == "__main__":
    a = AppConfig()
    b = AppConfig()
    assert a is b
    print("Same object:", a is b)
    print("Initial DB URL:", a.db_url)
    a.reload_from_env()
    print("After reload DB URL:", b.db_url)