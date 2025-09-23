class DatabaseConnection:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.connection_string = "database://localhost:5432"
        return cls._instance
    
    def connect(self):
        return f"Connected to {self.connection_string}"

if __name__ == "__main__":
    db1 = DatabaseConnection()
    db2 = DatabaseConnection()
    
    print(db1.connect())
    print(db2.connect())
    print(f"Same instance: {db1 is db2}")
    
    db1.connection_string = "database://remote:3306"
    print(f"db2 connection: {db2.connection_string}")