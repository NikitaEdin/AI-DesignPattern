import time
from typing import Dict, Any

class DatabaseConnection:
    def __init__(self):
        time.sleep(0.1)  # Simulate connection delay
        self._connected = True
    
    def query(self, sql: str) -> str:
        if not self._connected:
            raise ConnectionError("Database connection lost")
        return f"Result for: {sql}"
    
    def close(self):
        self._connected = False

class ConnectionManager:
    def __init__(self):
        self._connection = None
        self._query_cache: Dict[str, str] = {}
        self._query_count = 0
    
    def query(self, sql: str) -> str:
        if sql in self._query_cache:
            return f"[CACHED] {self._query_cache[sql]}"
        
        if not self._connection:
            self._connection = DatabaseConnection()
        
        try:
            result = self._connection.query(sql)
            self._query_cache[sql] = result
            self._query_count += 1
            return result
        except ConnectionError:
            self._connection = DatabaseConnection()
            result = self._connection.query(sql)
            self._query_cache[sql] = result
            self._query_count += 1
            return result
    
    def get_stats(self) -> Dict[str, Any]:
        return {
            "total_queries": self._query_count,
            "cached_queries": len(self._query_cache),
            "connected": self._connection is not None
        }

if __name__ == "__main__":
    manager = ConnectionManager()
    
    print(manager.query("SELECT * FROM users"))
    print(manager.query("SELECT * FROM orders"))
    print(manager.query("SELECT * FROM users"))
    
    print(f"Stats: {manager.get_stats()}")