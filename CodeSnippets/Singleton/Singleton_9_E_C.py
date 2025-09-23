class DatabaseConnection:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
            cls._instance.connection_string = "localhost:5432"
        return cls._instance
    
    def get_connection(self):
        return self.connection_string
    
    def set_connection(self, connection):
        self.connection_string = connection

if __name__ == "__main__":
    db1 = DatabaseConnection()
    db2 = DatabaseConnection()
    
    print(f"db1 connection: {db1.get_connection()}")
    print(f"db2 connection: {db2.get_connection()}")
    print(f"Same instance: {db1 is db2}")
    
    db1.set_connection("remote:3306")
    print(f"After change - db2 connection: {db2.get_connection()}")