import time
from typing import Optional

class DatabaseService:
    def __init__(self):
        self._connected = False
    
    def connect(self):
        print("Connecting to database...")
        time.sleep(1)
        self._connected = True
    
    def fetch_data(self, query: str) -> str:
        if not self._connected:
            raise ConnectionError("Not connected to database")
        print(f"Executing query: {query}")
        return f"Result for: {query}"
    
    def disconnect(self):
        self._connected = False
        print("Disconnected from database")

class CachedDatabaseService:
    def __init__(self):
        self._service: Optional[DatabaseService] = None
        self._cache = {}
    
    def _get_service(self) -> DatabaseService:
        if self._service is None:
            self._service = DatabaseService()
            self._service.connect()
        return self._service
    
    def fetch_data(self, query: str) -> str:
        if query in self._cache:
            print(f"Cache hit for: {query}")
            return self._cache[query]
        
        try:
            service = self._get_service()
            result = service.fetch_data(query)
            self._cache[query] = result
            return result
        except ConnectionError as e:
            return f"Error: {e}"
    
    def clear_cache(self):
        self._cache.clear()
        print("Cache cleared")

if __name__ == "__main__":
    db = CachedDatabaseService()
    
    print(db.fetch_data("SELECT * FROM users"))
    print(db.fetch_data("SELECT * FROM orders"))
    print(db.fetch_data("SELECT * FROM users"))
    
    db.clear_cache()
    print(db.fetch_data("SELECT * FROM users"))