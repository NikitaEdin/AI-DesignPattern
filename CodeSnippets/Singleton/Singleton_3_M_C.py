class DatabaseConnection:
    _instance = None
    _lock = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        if DatabaseConnection._lock:
            raise RuntimeError("Cannot create multiple instances")
        
        DatabaseConnection._lock = True
        self.host = "localhost"
        self.port = 5432
        self.database = "myapp"
        self.connection_pool = []
        self.is_connected = False
        self._initialized = True
        DatabaseConnection._lock = False
    
    def connect(self):
        if not self.is_connected:
            self.is_connected = True
            return f"Connected to {self.database} at {self.host}:{self.port}"
        return "Already connected"
    
    def disconnect(self):
        if self.is_connected:
            self.is_connected = False
            self.connection_pool.clear()
            return "Disconnected from database"
        return "Not connected"
    
    def execute_query(self, query):
        if not self.is_connected:
            raise ConnectionError("Database not connected")
        return f"Executed: {query}"

if __name__ == "__main__":
    db1 = DatabaseConnection()
    print(db1.connect())
    
    db2 = DatabaseConnection()
    print(f"Same instance: {db1 is db2}")
    
    print(db2.execute_query("SELECT * FROM users"))
    print(db1.disconnect())
    
    try:
        db2.execute_query("SELECT * FROM products")
    except ConnectionError as e:
        print(f"Error: {e}")