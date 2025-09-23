import threading

_instances = {}
_lock = threading.Lock()

class ConfigurationManager:
    def __new__(cls):
        if cls not in _instances:
            with _lock:
                if cls not in _instances:
                    _instances[cls] = super(ConfigurationManager, cls).__new__(cls)
                    _instances[cls]._initialized = False
        return _instances[cls]

    def __init__(self):
        if not hasattr(self, '_initialized') or not self._initialized:
            self.settings = {}
            self._initialized = True

    def set_setting(self, key, value):
        if not isinstance(key, str):
            raise ValueError("Key must be a string")
        self.settings[key] = value

    def get_setting(self, key, default=None):
        return self.settings.get(key, default)

    def has_setting(self, key):
        return key in self.settings

    def clear_settings(self):
        self.settings.clear()

class DatabaseConfig(ConfigurationManager):
    def __init__(self):
        super().__init__()
        if not self.has_setting('connection_string'):
            self.set_setting('connection_string', 'default_db')

    def validate_connection(self):
        conn_str = self.get_setting('connection_string')
        if not conn_str or 'db' not in conn_str.lower():
            raise ValueError("Invalid connection string")

def worker_thread(cls):
    instance = cls()
    instance.set_setting('thread_id', threading.current_thread().name)
    print(f"From {threading.current_thread().name}: ID {id(instance)}, setting: {instance.get_setting('debug', 'not set')}")

if __name__ == "__main__":
    mgr1 = ConfigurationManager()
    mgr1.set_setting('debug', True)
    print(f"Main thread: ID {id(mgr1)}, debug: {mgr1.get_setting('debug')}")

    db1 = DatabaseConfig()
    db1.set_setting('host', 'localhost')
    print(f"DB Main: ID {id(db1)}, host: {db1.get_setting('host')}, conn: {db1.get_setting('connection_string')}")

    threads = []
    for i in range(3):
        t = threading.Thread(target=worker_thread, args=(ConfigurationManager,))
        t.start()
        threads.append(t)

    db_threads = []
    for i in range(2):
        dt = threading.Thread(target=worker_thread, args=(DatabaseConfig,))
        dt.start()
        db_threads.append(dt)

    for t in threads + db_threads:
        t.join()

    mgr2 = ConfigurationManager()
    print(f"After threads: ID {id(mgr2)}, debug: {mgr2.get_setting('debug')}, same as first: {mgr1 is mgr2}")

    db2 = DatabaseConfig()
    print(f"DB After: ID {id(db2)}, host: {db2.get_setting('host')}, same as first DB: {db1 is db2}")

    try:
        db2.validate_connection()
        print("DB validation passed")
    except ValueError as e:
        print(f"DB validation error: {e}")