class DatabaseManager:
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self.connection_string = "postgresql://localhost:5432/mydb"
            self.active_connections = 0
            self.max_connections = 10
            self._initialized = True
    
    def connect(self):
        if self.active_connections >= self.max_connections:
            raise ConnectionError("Maximum connections reached")
        self.active_connections += 1
        return f"Connection {self.active_connections} established to {self.connection_string}"
    
    def disconnect(self):
        if self.active_connections > 0:
            self.active_connections -= 1
        return f"Connection closed. Active connections: {self.active_connections}"
    
    def get_status(self):
        return {
            "active_connections": self.active_connections,
            "max_connections": self.max_connections,
            "connection_string": self.connection_string
        }

if __name__ == "__main__":
    db1 = DatabaseManager()
    db2 = DatabaseManager()
    
    print(f"Same instance: {db1 is db2}")
    
    print(db1.connect())
    print(db2.connect())
    
    print(f"DB1 status: {db1.get_status()}")
    print(f"DB2 status: {db2.get_status()}")
    
    print(db1.disconnect())
    print(f"Final status: {db2.get_status()}")