class DatabaseConnection:
    def __init__(self, connection_string):
        self.connection_string = connection_string
        self.connected = False
        print(f"Establishing database connection to {connection_string}")
    
    def connect(self):
        if not self.connected:
            print("Connecting to database...")
            self.connected = True
    
    def query(self, sql):
        if not self.connected:
            raise RuntimeError("Database not connected")
        return f"Result for: {sql}"
    
    def disconnect(self):
        if self.connected:
            print("Disconnecting from database")
            self.connected = False

class DatabaseManager:
    def __init__(self, connection_string):
        self.connection_string = connection_string
        self._connection = None
        self._query_cache = {}
    
    def _get_connection(self):
        if self._connection is None:
            self._connection = DatabaseConnection(self.connection_string)
            self._connection.connect()
        return self._connection
    
    def query(self, sql):
        if sql in self._query_cache:
            print(f"Cache hit for: {sql}")
            return self._query_cache[sql]
        
        connection = self._get_connection()
        result = connection.query(sql)
        self._query_cache[sql] = result
        print(f"Query executed and cached: {sql}")
        return result
    
    def disconnect(self):
        if self._connection:
            self._connection.disconnect()
            self._connection = None

if __name__ == "__main__":
    db_manager = DatabaseManager("postgresql://localhost:5432/mydb")
    
    result1 = db_manager.query("SELECT * FROM users")
    print(result1)
    
    result2 = db_manager.query("SELECT * FROM users")
    print(result2)
    
    result3 = db_manager.query("SELECT * FROM products")
    print(result3)
    
    db_manager.disconnect()