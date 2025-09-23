class DatabaseConnection:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
            cls._instance.connection_id = "DB_12345"
        return cls._instance
    
    def get_connection_id(self):
        return self.connection_id
    
    def execute_query(self, query):
        return f"Executing: {query} on {self.connection_id}"

if __name__ == "__main__":
    db1 = DatabaseConnection()
    db2 = DatabaseConnection()
    
    print(f"db1 ID: {db1.get_connection_id()}")
    print(f"db2 ID: {db2.get_connection_id()}")
    print(f"Same instance: {db1 is db2}")
    print(db1.execute_query("SELECT * FROM users"))