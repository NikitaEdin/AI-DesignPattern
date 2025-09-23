class DatabaseConnection:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.connected = False
    
    def connect(self):
        print(f"Establishing connection to {self.host}:{self.port}")
        self.connected = True
    
    def execute_query(self, query):
        if not self.connected:
            raise ConnectionError("Database not connected")
        print(f"Executing query: {query}")
        return f"Result for: {query}"
    
    def disconnect(self):
        print("Closing database connection")
        self.connected = False

class DatabaseGateway:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self._connection = None
        self._query_cache = {}
    
    def _get_connection(self):
        if self._connection is None:
            self._connection = DatabaseConnection(self.host, self.port)
            self._connection.connect()
        return self._connection
    
    def execute_query(self, query):
        if query in self._query_cache:
            print(f"Cache hit for: {query}")
            return self._query_cache[query]
        
        connection = self._get_connection()
        result = connection.execute_query(query)
        self._query_cache[query] = result
        return result
    
    def disconnect(self):
        if self._connection:
            self._connection.disconnect()
            self._connection = None

if __name__ == "__main__":
    gateway = DatabaseGateway("localhost", 5432)
    
    result1 = gateway.execute_query("SELECT * FROM users")
    result2 = gateway.execute_query("SELECT * FROM users")
    result3 = gateway.execute_query("SELECT * FROM products")
    
    gateway.disconnect()