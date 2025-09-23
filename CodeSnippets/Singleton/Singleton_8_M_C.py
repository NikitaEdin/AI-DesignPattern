class DatabaseConnection:
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self.connection_string = "localhost:5432/mydb"
            self.is_connected = False
            self._query_count = 0
            DatabaseConnection._initialized = True
    
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
        self._query_count += 1
        return f"Executed: {query} (Total queries: {self._query_count})"
    
    def get_stats(self):
        return {
            "connected": self.is_connected,
            "queries_executed": self._query_count,
            "connection_string": self.connection_string
        }

if __name__ == "__main__":
    db1 = DatabaseConnection()
    db2 = DatabaseConnection()
    
    print(f"Same instance: {db1 is db2}")
    
    print(db1.connect())
    print(db1.execute_query("SELECT * FROM users"))
    print(db2.execute_query("SELECT * FROM products"))
    
    print(f"Stats from db1: {db1.get_stats()}")
    print(f"Stats from db2: {db2.get_stats()}")
    
    print(db2.disconnect())