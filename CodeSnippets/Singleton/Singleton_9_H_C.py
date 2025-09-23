import threading
from typing import Any, Dict, Optional

class DatabaseManager:
    _instances: Dict[str, 'DatabaseManager'] = {}
    _lock = threading.Lock()
    _initialized = set()
    
    def __new__(cls, connection_string: str = "default"):
        if connection_string not in cls._instances:
            with cls._lock:
                if connection_string not in cls._instances:
                    instance = super().__new__(cls)
                    cls._instances[connection_string] = instance
        return cls._instances[connection_string]
    
    def __init__(self, connection_string: str = "default"):
        if id(self) not in self._initialized:
            self.connection_string = connection_string
            self.connections = []
            self.is_connected = False
            self._data = {}
            self._lock_instance = threading.Lock()
            self._initialized.add(id(self))
    
    def connect(self):
        with self._lock_instance:
            if not self.is_connected:
                self.is_connected = True
                return f"Connected to {self.connection_string}"
            return f"Already connected to {self.connection_string}"
    
    def disconnect(self):
        with self._lock_instance:
            if self.is_connected:
                self.is_connected = False
                self.connections.clear()
                return f"Disconnected from {self.connection_string}"
            return "Not connected"
    
    def query(self, sql: str) -> str:
        if not self.is_connected:
            return "Error: Not connected to database"
        return f"Executing: {sql} on {self.connection_string}"
    
    def set_data(self, key: str, value: Any):
        with self._lock_instance:
            self._data[key] = value
    
    def get_data(self, key: str) -> Any:
        return self._data.get(key)
    
    @classmethod
    def get_instance(cls, connection_string: str = "default") -> 'DatabaseManager':
        return cls(connection_string)
    
    @classmethod
    def reset_instances(cls):
        with cls._lock:
            cls._instances.clear()
            cls._initialized.clear()

class ConfigurationManager:
    _instance: Optional['ConfigurationManager'] = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        self.settings = {
            "debug": False,
            "max_connections": 100,
            "timeout": 30
        }
        self._lock_instance = threading.Lock()
    
    def get_setting(self, key: str) -> Any:
        return self.settings.get(key)
    
    def set_setting(self, key: str, value: Any):
        with self._lock_instance:
            self.settings[key] = value
    
    def load_from_file(self, filename: str):
        with self._lock_instance:
            self.settings["loaded_from"] = filename
            return f"Configuration loaded from {filename}"

if __name__ == "__main__":
    db1 = DatabaseManager("production")
    db2 = DatabaseManager("production")
    db3 = DatabaseManager("test")
    
    print(f"db1 is db2: {db1 is db2}")
    print(f"db1 is db3: {db1 is db3}")
    
    print(db1.connect())
    print(db2.connect())
    print(db3.connect())
    
    db1.set_data("user_count", 1000)
    print(f"User count from db2: {db2.get_data('user_count')}")
    
    config1 = ConfigurationManager()
    config2 = ConfigurationManager()
    
    print(f"config1 is config2: {config1 is config2}")
    
    config1.set_setting("debug", True)
    print(f"Debug setting from config2: {config2.get_setting('debug')}")
    
    def worker(name):
        db = DatabaseManager.get_instance("worker_db")
        config = ConfigurationManager()
        return f"{name}: DB connected: {db.is_connected}, Debug: {config.get_setting('debug')}"
    
    import concurrent.futures
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        futures = [executor.submit(worker, f"Thread-{i}") for i in range(3)]
        for future in concurrent.futures.as_completed(futures):
            print(future.result())