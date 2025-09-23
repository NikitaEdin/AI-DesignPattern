class DatabaseConnection:
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self.connection_string = "database://localhost:5432/myapp"
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
        return "Not connected"
    
    def execute_query(self, query):
        if not self.is_connected:
            raise ConnectionError("Database not connected")
        self._query_count += 1
        return f"Executed: {query} (Total queries: {self._query_count})"
    
    def get_stats(self):
        status = "Connected" if self.is_connected else "Disconnected"
        return f"Status: {status}, Queries executed: {self._query_count}"

if __name__ == "__main__":
    db1 = DatabaseConnection()
    db2 = DatabaseConnection()
    
    print(f"Same instance: {db1 is db2}")
    
    print(db1.connect())
    print(db1.execute_query("SELECT * FROM users"))
    print(db2.execute_query("INSERT INTO users VALUES (1, 'John')"))
    
    print(f"DB1 stats: {db1.get_stats()}")
    print(f"DB2 stats: {db2.get_stats()}")
    
    print(db2.disconnect())
    print(f"DB1 connected: {db1.is_connected}")