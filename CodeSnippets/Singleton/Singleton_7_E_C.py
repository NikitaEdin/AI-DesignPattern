class DatabaseConnection:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.connection_id = "DB_001"
            self.initialized = True
    
    def get_connection(self):
        return f"Connection: {self.connection_id}"

if __name__ == "__main__":
    db1 = DatabaseConnection()
    db2 = DatabaseConnection()
    
    print(db1.get_connection())
    print(db2.get_connection())
    print(f"Same instance: {db1 is db2}")