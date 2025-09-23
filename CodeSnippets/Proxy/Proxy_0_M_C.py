import time
from abc import ABC, abstractmethod

class DatabaseInterface(ABC):
    @abstractmethod
    def query(self, sql: str) -> str:
        pass

class RealDatabase(DatabaseInterface):
    def __init__(self):
        time.sleep(2)
        print("Database connection established")
    
    def query(self, sql: str) -> str:
        print(f"Executing: {sql}")
        return f"Results for: {sql}"

class DatabaseGateway(DatabaseInterface):
    def __init__(self):
        self._database = None
        self._cache = {}
    
    def query(self, sql: str) -> str:
        if sql in self._cache:
            print("Cache hit - returning cached result")
            return self._cache[sql]
        
        if self._database is None:
            print("Initializing database connection...")
            self._database = RealDatabase()
        
        result = self._database.query(sql)
        self._cache[sql] = result
        return result

if __name__ == "__main__":
    gateway = DatabaseGateway()
    
    print("First query:")
    result1 = gateway.query("SELECT * FROM users")
    print(result1)
    
    print("\nSecond query (same):")
    result2 = gateway.query("SELECT * FROM users")
    print(result2)
    
    print("\nThird query (different):")
    result3 = gateway.query("SELECT * FROM orders")
    print(result3)