class DatabaseService:
    def __init__(self):
        self.connected = False
    
    def connect(self):
        self.connected = True
        print("Connected to database")
    
    def query(self, sql):
        if not self.connected:
            raise ConnectionError("Database not connected")
        return f"Result for: {sql}"

class DatabaseGateway:
    def __init__(self):
        self._service = None
        self._cache = {}
    
    def _get_service(self):
        if self._service is None:
            self._service = DatabaseService()
            self._service.connect()
        return self._service
    
    def query(self, sql):
        if sql in self._cache:
            print(f"Cache hit for: {sql}")
            return self._cache[sql]
        
        try:
            service = self._get_service()
            result = service.query(sql)
            self._cache[sql] = result
            print(f"Query executed and cached: {sql}")
            return result
        except ConnectionError as e:
            return f"Error: {e}"

if __name__ == "__main__":
    gateway = DatabaseGateway()
    
    result1 = gateway.query("SELECT * FROM users")
    print(result1)
    
    result2 = gateway.query("SELECT * FROM users")
    print(result2)
    
    result3 = gateway.query("SELECT * FROM orders")
    print(result3)