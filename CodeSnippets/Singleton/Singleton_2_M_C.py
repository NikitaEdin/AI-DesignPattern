class DatabaseConnection:
    _instance = None
    _lock = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._lock:
            self.host = "localhost"
            self.port = 5432
            self.database = "myapp"
            self.connected = False
            self.__class__._lock = True
    
    def connect(self):
        if not self.connected:
            try:
                self.connected = True
                return f"Connected to {self.database} at {self.host}:{self.port}"
            except Exception as e:
                return f"Connection failed: {e}"
        return "Already connected"
    
    def disconnect(self):
        if self.connected:
            self.connected = False
            return "Disconnected from database"
        return "Not connected"
    
    def execute_query(self, query):
        if not self.connected:
            return "Error: Not connected to database"
        return f"Executing: {query}"
    
    def get_status(self):
        status = "connected" if self.connected else "disconnected"
        return f"Database {self.database} is {status}"

if __name__ == "__main__":
    db1 = DatabaseConnection()
    db2 = DatabaseConnection()
    
    print(f"Same instance: {db1 is db2}")
    
    print(db1.connect())
    print(db2.get_status())
    
    result = db1.execute_query("SELECT * FROM users")
    print(result)
    
    print(db2.disconnect())
    print(db1.get_status())