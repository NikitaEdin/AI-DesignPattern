import time
from typing import Dict, Any

class DatabaseService:
    def __init__(self):
        self._connected = False
        
    def connect(self):
        print("Establishing database connection...")
        time.sleep(1)
        self._connected = True
        
    def query(self, sql: str) -> str:
        if not self._connected:
            self.connect()
        print(f"Executing query: {sql}")
        return f"Result for: {sql}"
        
    def disconnect(self):
        self._connected = False
        print("Database connection closed")

class CachedDatabaseService:
    def __init__(self, service: DatabaseService):
        self._service = service
        self._cache: Dict[str, str] = {}
        
    def query(self, sql: str) -> str:
        if sql in self._cache:
            print(f"Cache hit for: {sql}")
            return self._cache[sql]
            
        try:
            result = self._service.query(sql)
            self._cache[sql] = result
            print(f"Result cached for: {sql}")
            return result
        except Exception as e:
            print(f"Query failed: {e}")
            return "Query error"
            
    def clear_cache(self):
        self._cache.clear()
        print("Cache cleared")

if __name__ == "__main__":
    real_db = DatabaseService()
    cached_db = CachedDatabaseService(real_db)
    
    result1 = cached_db.query("SELECT * FROM users")
    result2 = cached_db.query("SELECT * FROM users")
    result3 = cached_db.query("SELECT * FROM products")
    
    cached_db.clear_cache()
    result4 = cached_db.query("SELECT * FROM users")