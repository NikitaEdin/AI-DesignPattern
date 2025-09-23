class DatabaseConnection:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.initialized = True
            self.connection_string = "database://localhost:5432"

def main():
    connection1 = DatabaseConnection()
    connection2 = DatabaseConnection()
    
    print(f"Connection 1 ID: {id(connection1)}")
    print(f"Connection 2 ID: {id(connection2)}")
    print(f"Are they the same object? {connection1 is connection2}")
    
    print(f"Connection string: {connection1.connection_string}")

if __name__ == "__main__":
    main()