class DatabaseConnection:
    _instance = None
    _initialized = False
    
    def __new__(cls, host="localhost", port=5432):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, host="localhost", port=5432):
        if not self._initialized:
            self.host = host
            self.port = port
            self.connection_count = 0
            self._initialized = True
    
    def connect(self):
        self.connection_count += 1
        return f"Connected to {self.host}:{self.port} (connection #{self.connection_count})"
    
    def get_status(self):
        return f"Host: {self.host}, Port: {self.port}, Total connections: {self.connection_count}"


if __name__ == "__main__":
    db1 = DatabaseConnection("db1.example.com", 5432)
    print(db1.connect())
    
    db2 = DatabaseConnection("db2.example.com", 3306)
    print(db2.connect())
    
    print(db1.get_status())
    print(db2.get_status())
    print(f"Same instance: {db1 is db2}")