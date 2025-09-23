import time
from abc import ABC, abstractmethod

class DatabaseInterface(ABC):
    @abstractmethod
    def query(self, sql):
        pass

class RealDatabase(DatabaseInterface):
    def __init__(self):
        self.connection_time = 2
        self.connected = False
    
    def connect(self):
        if not self.connected:
            time.sleep(self.connection_time)
            self.connected = True
    
    def query(self, sql):
        self.connect()
        return f"Executing query: {sql}"

class DatabaseGateway(DatabaseInterface):
    def __init__(self):
        self._database = None
        self._cache = {}
        self._access_count = 0
    
    def query(self, sql):
        self._access_count += 1
        
        if not self._has_access():
            raise PermissionError("Access denied: Too many requests")
        
        if sql in self._cache:
            return f"[CACHED] {self._cache[sql]}"
        
        if self._database is None:
            self._database = RealDatabase()
        
        result = self._database.query(sql)
        self._cache[sql] = result
        return result
    
    def _has_access(self):
        return self._access_count <= 5

if __name__ == "__main__":
    db = DatabaseGateway()
    
    queries = ["SELECT * FROM users", "SELECT * FROM orders", "SELECT * FROM users"]
    
    for query in queries:
        try:
            result = db.query(query)
            print(result)
        except PermissionError as e:
            print(f"Error: {e}")
    
    for i in range(4):
        try:
            result = db.query(f"SELECT * FROM table_{i}")
            print(result)
        except PermissionError as e:
            print(f"Error: {e}")