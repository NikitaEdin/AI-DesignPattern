class DatabaseManager:
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self.connection_string = "postgresql://localhost:5432/mydb"
            self.connected = False
            self.query_count = 0
            self.__class__._initialized = True
    
    def connect(self):
        if not self.connected:
            self.connected = True
            return f"Connected to {self.connection_string}"
        return "Already connected"
    
    def execute_query(self, query):
        if not self.connected:
            raise ConnectionError("Database not connected")
        self.query_count += 1
        return f"Executed: {query} (Query #{self.query_count})"
    
    def disconnect(self):
        if self.connected:
            self.connected = False
            return "Disconnected from database"
        return "Not connected"
    
    def get_stats(self):
        return {
            "connected": self.connected,
            "queries_executed": self.query_count,
            "connection_string": self.connection_string
        }

if __name__ == "__main__":
    db1 = DatabaseManager()
    db2 = DatabaseManager()
    
    print(f"Same instance: {db1 is db2}")
    
    db1.connect()
    print(db1.execute_query("SELECT * FROM users"))
    print(db2.execute_query("SELECT * FROM orders"))
    
    print(f"DB1 stats: {db1.get_stats()}")
    print(f"DB2 stats: {db2.get_stats()}")
    
    db2.disconnect()
    print(f"DB1 connected: {db1.connected}")