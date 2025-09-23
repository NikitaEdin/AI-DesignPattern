class DatabaseConnection:
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self.host = "localhost"
            self.port = 5432
            self.database = "myapp"
            self.connection_count = 0
            self._initialized = True
    
    def connect(self):
        if self.connection_count == 0:
            print(f"Establishing connection to {self.database} at {self.host}:{self.port}")
            self.connection_count += 1
            return True
        else:
            print("Using existing connection")
            return True
    
    def disconnect(self):
        if self.connection_count > 0:
            print("Closing database connection")
            self.connection_count = 0
            return True
        return False
    
    def get_connection_info(self):
        return {
            "host": self.host,
            "port": self.port,
            "database": self.database,
            "active": self.connection_count > 0
        }

if __name__ == "__main__":
    db1 = DatabaseConnection()
    db2 = DatabaseConnection()
    
    print(f"Same instance: {db1 is db2}")
    
    db1.connect()
    print(f"DB1 info: {db1.get_connection_info()}")
    print(f"DB2 info: {db2.get_connection_info()}")
    
    db2.disconnect()
    print(f"After disconnect - DB1 info: {db1.get_connection_info()}")