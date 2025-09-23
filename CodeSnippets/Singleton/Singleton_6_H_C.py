import threading
import weakref
from functools import wraps

def ensure_initialized(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if not self._initialized:
            raise RuntimeError("Instance not properly initialized")
        return func(self, *args, **kwargs)
    return wrapper

class DatabaseConnection:
    _instance = None
    _lock = threading.Lock()
    _instances = weakref.WeakSet()
    _initialized = False
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instances.add(cls._instance)
        return cls._instance
    
    def __init__(self, host="localhost", port=5432, database="mydb"):
        if self._initialized:
            return
        
        with self._lock:
            if not self._initialized:
                self.host = host
                self.port = port
                self.database = database
                self.connection_pool = []
                self._connection_count = 0
                self._initialized = True
    
    @ensure_initialized
    def connect(self):
        self._connection_count += 1
        connection_id = f"conn_{self._connection_count}"
        self.connection_pool.append(connection_id)
        return connection_id
    
    @ensure_initialized
    def disconnect(self, connection_id):
        if connection_id in self.connection_pool:
            self.connection_pool.remove(connection_id)
            return True
        return False
    
    @ensure_initialized
    def get_connection_info(self):
        return {
            'host': self.host,
            'port': self.port,
            'database': self.database,
            'active_connections': len(self.connection_pool),
            'total_connections_created': self._connection_count
        }
    
    @classmethod
    def get_instance_count(cls):
        return len(cls._instances)
    
    @classmethod
    def reset_instance(cls):
        with cls._lock:
            cls._instance = None
            cls._initialized = False

class ConfigurationManager:
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._config = {}
                    cls._instance._initialized = True
        return cls._instance
    
    def set_config(self, key, value):
        with self._lock:
            self._config[key] = value
    
    def get_config(self, key, default=None):
        return self._config.get(key, default)
    
    def get_all_config(self):
        return dict(self._config)

def thread_test_function(results, thread_id):
    db = DatabaseConnection("remote_host", 3306, f"db_{thread_id}")
    conn = db.connect()
    results[thread_id] = {
        'instance_id': id(db),
        'connection': conn,
        'info': db.get_connection_info()
    }

if __name__ == "__main__":
    db1 = DatabaseConnection("localhost", 5432, "primary_db")
    db2 = DatabaseConnection("different_host", 3306, "secondary_db")
    
    print(f"Same instance: {db1 is db2}")
    print(f"Instance ID 1: {id(db1)}")
    print(f"Instance ID 2: {id(db2)}")
    
    conn1 = db1.connect()
    conn2 = db2.connect()
    
    print(f"DB1 info: {db1.get_connection_info()}")
    print(f"DB2 info: {db2.get_connection_info()}")
    
    config1 = ConfigurationManager()
    config2 = ConfigurationManager()
    
    config1.set_config("api_url", "https://api.example.com")
    config1.set_config("timeout", 30)
    
    print(f"Config instances same: {config1 is config2}")
    print(f"Config from config2: {config2.get_all_config()}")
    
    import threading
    results = {}
    threads = []
    
    for i in range(3):
        thread = threading.Thread(target=thread_test_function, args=(results, i))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    
    print("\nThread test results:")
    for thread_id, result in results.items():
        print(f"Thread {thread_id}: Instance ID {result['instance_id']}")
    
    all_same = len(set(result['instance_id'] for result in results.values())) == 1
    print(f"All threads got same instance: {all_same}")
    
    print(f"Total instance count: {DatabaseConnection.get_instance_count()}")