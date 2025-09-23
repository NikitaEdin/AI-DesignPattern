import threading
from typing import Type, Any, Dict, Optional


class UniqueMeta(type):
    _instances: Dict[Type, Any] = {}
    _locks: Dict[Type, threading.Lock] = {}
    _main_lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        if cls not in cls._locks:
            with cls._main_lock:
                if cls not in cls._locks:
                    cls._locks[cls] = threading.Lock()

        if cls not in cls._instances:
            with cls._locks[cls]:
                if cls not in cls._instances:
                    instance = super().__call__(*args, **kwargs)
                    cls._instances[cls] = instance
        return cls._instances[cls]

    def reset_instance(cls):
        with cls._main_lock:
            if cls in cls._instances:
                with cls._locks[cls]:
                    if cls in cls._instances:
                        del cls._instances[cls]


class DatabaseManager(metaclass=UniqueMeta):
    def __init__(self):
        if hasattr(self, '_initialized'):
            return
        self._initialized = True
        self.connection_pool = []
        self.active_connections = 0
        self._lock = threading.Lock()

    def connect(self):
        with self._lock:
            self.active_connections += 1
            connection_id = f"conn_{self.active_connections}"
            self.connection_pool.append(connection_id)
            return connection_id

    def disconnect(self, connection_id: str):
        with self._lock:
            if connection_id in self.connection_pool:
                self.connection_pool.remove(connection_id)

    def get_status(self):
        return {
            'active_connections': len(self.connection_pool),
            'pool_size': len(self.connection_pool)
        }


class ConfigurationManager(metaclass=UniqueMeta):
    def __init__(self):
        if hasattr(self, '_initialized'):
            return
        self._initialized = True
        self._config = {}
        self._lock = threading.Lock()

    def set_config(self, key: str, value: Any):
        with self._lock:
            self._config[key] = value

    def get_config(self, key: str, default=None):
        return self._config.get(key, default)

    def get_all_config(self):
        return self._config.copy()


def test_thread_safety():
    import concurrent.futures
    
    instances = []
    
    def create_instance():
        return DatabaseManager()
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(create_instance) for _ in range(20)]
        instances = [future.result() for future in futures]
    
    return len(set(id(instance) for instance in instances)) == 1


if __name__ == "__main__":
    db1 = DatabaseManager()
    db2 = DatabaseManager()
    
    print(f"Same instance: {db1 is db2}")
    
    conn1 = db1.connect()
    conn2 = db2.connect()
    
    print(f"DB1 status: {db1.get_status()}")
    print(f"DB2 status: {db2.get_status()}")
    
    config1 = ConfigurationManager()
    config2 = ConfigurationManager()
    
    config1.set_config("database_url", "localhost:5432")
    config1.set_config("timeout", 30)
    
    print(f"Same config instance: {config1 is config2}")
    print(f"Config from config2: {config2.get_all_config()}")
    
    print(f"Thread safety test passed: {test_thread_safety()}")
    
    DatabaseManager.reset_instance()
    db3 = DatabaseManager()
    print(f"New instance after reset: {db3 is db1}")
    print(f"New instance status: {db3.get_status()}")