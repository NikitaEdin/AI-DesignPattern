class DatabaseConnection:
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self.connection_string = "localhost:5432"
            self.is_connected = False
            self._queries_executed = 0
            self._initialized = True
    
    def connect(self):
        if not self.is_connected:
            self.is_connected = True
            return f"Connected to {self.connection_string}"
        return "Already connected"
    
    def disconnect(self):
        if self.is_connected:
            self.is_connected = False
            return "Disconnected from database"
        return "Already disconnected"
    
    def execute_query(self, query):
        if not self.is_connected:
            raise ConnectionError("Database not connected")
        self._queries_executed += 1
        return f"Executed: {query} (Total queries: {self._queries_executed})"
    
    def get_stats(self):
        return {
            "connected": self.is_connected,
            "queries_executed": self._queries_executed,
            "connection_string": self.connection_string
        }

if __name__ == "__main__":
    db1 = DatabaseConnection()
    db2 = DatabaseConnection()
    
    print(f"Same instance: {db1 is db2}")
    
    print(db1.connect())
    print(db1.execute_query("SELECT * FROM users"))
    print(db2.execute_query("SELECT * FROM products"))
    
    print(f"DB1 stats: {db1.get_stats()}")
    print(f"DB2 stats: {db2.get_stats()}")
    
    print(db2.disconnect())
    print(f"DB1 connected: {db1.is_connected}")