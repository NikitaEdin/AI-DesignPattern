class DatabaseManager:
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not DatabaseManager._initialized:
            self.connection_string = "localhost:5432"
            self.active_connections = 0
            self.max_connections = 10
            DatabaseManager._initialized = True
    
    def connect(self):
        if self.active_connections < self.max_connections:
            self.active_connections += 1
            return f"Connection established. Active: {self.active_connections}"
        else:
            raise Exception("Maximum connections reached")
    
    def disconnect(self):
        if self.active_connections > 0:
            self.active_connections -= 1
            return f"Connection closed. Active: {self.active_connections}"
        return "No active connections to close"
    
    def get_status(self):
        return {
            "connection_string": self.connection_string,
            "active_connections": self.active_connections,
            "max_connections": self.max_connections
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