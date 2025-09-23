import threading
import weakref
from typing import Dict, Any, Optional

class UniqueInstance:
    _instances: Dict[type, Any] = {}
    _lock = threading.RLock()
    _initialized = weakref.WeakSet()
    
    def __new__(cls, *args, **kwargs):
        if cls not in cls._instances:
            with cls._lock:
                if cls not in cls._instances:
                    instance = super().__new__(cls)
                    cls._instances[cls] = instance
        return cls._instances[cls]
    
    def __init__(self, *args, **kwargs):
        if self not in self._initialized:
            with self._lock:
                if self not in self._initialized:
                    self._setup(*args, **kwargs)
                    self._initialized.add(self)
    
    def _setup(self, *args, **kwargs):
        pass
    
    @classmethod
    def get_instance(cls, *args, **kwargs):
        return cls(*args, **kwargs)
    
    @classmethod
    def clear_instances(cls):
        with cls._lock:
            cls._instances.clear()
            cls._initialized.clear()

class DatabaseManager(UniqueInstance):
    def _setup(self, connection_string: str = "localhost:5432"):
        self.connection_string = connection_string
        self.connections = []
        self.is_connected = False
    
    def connect(self):
        if not self.is_connected:
            self.is_connected = True
            return f"Connected to {self.connection_string}"
        return "Already connected"
    
    def execute_query(self, query: str):
        if self.is_connected:
            return f"Executing: {query}"
        return "Not connected to database"
    
    def get_connection_count(self):
        return len(self.connections)

class ConfigurationManager(UniqueInstance):
    def _setup(self, config_file: Optional[str] = None):
        self._config = {}
        self.config_file = config_file or "default.conf"
        self._load_defaults()
    
    def _load_defaults(self):
        self._config.update({
            'debug': False,
            'max_connections': 100,
            'timeout': 30
        })
    
    def get(self, key: str, default=None):
        return self._config.get(key, default)
    
    def set(self, key: str, value: Any):
        self._config[key] = value
    
    def get_all_config(self):
        return self._config.copy()

def test_thread_safety():
    import concurrent.futures
    results = []
    
    def create_db_manager():
        return DatabaseManager("test_connection")
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(create_db_manager) for _ in range(20)]
        results = [future.result() for future in futures]
    
    return all(id(results[0]) == id(instance) for instance in results)

if __name__ == "__main__":
    db1 = DatabaseManager.get_instance("postgresql://localhost:5432")
    db2 = DatabaseManager("mysql://localhost:3306")
    
    print(f"Same instance: {db1 is db2}")
    print(f"Connection string: {db1.connection_string}")
    print(db1.connect())
    print(db2.execute_query("SELECT * FROM users"))
    
    config1 = ConfigurationManager()
    config2 = ConfigurationManager.get_instance("custom.conf")
    
    config1.set("debug", True)
    print(f"Same config instance: {config1 is config2}")
    print(f"Config debug value: {config2.get('debug')}")
    
    print(f"Thread safety test: {'PASSED' if test_thread_safety() else 'FAILED'}")
    
    UniqueInstance.clear_instances()
    db3 = DatabaseManager("new_connection")
    print(f"New instance after clear: {db3 is db1}")