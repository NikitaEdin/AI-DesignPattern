import time
from typing import Optional

class DatabaseConnection:
    def __init__(self, host: str):
        self.host = host
        self.connected = False
        print(f"Establishing connection to {host}...")
        time.sleep(0.1)
        self.connected = True
        print("Connection established")
    
    def query(self, sql: str) -> str:
        if not self.connected:
            raise ConnectionError("Not connected to database")
        print(f"Executing query: {sql}")
        return f"Result for: {sql}"
    
    def close(self):
        self.connected = False
        print("Connection closed")

class DatabaseGateway:
    def __init__(self, host: str):
        self.host = host
        self._connection: Optional[DatabaseConnection] = None
        self._query_cache = {}
    
    def query(self, sql: str) -> str:
        if sql in self._query_cache:
            print(f"Cache hit for: {sql}")
            return self._query_cache[sql]
        
        if not self._connection:
            self._connection = DatabaseConnection(self.host)
        
        result = self._connection.query(sql)
        self._query_cache[sql] = result
        return result
    
    def close(self):
        if self._connection:
            self._connection.close()
            self._connection = None
        self._query_cache.clear()

if __name__ == "__main__":
    db = DatabaseGateway("localhost:5432")
    
    print(db.query("SELECT * FROM users"))
    print(db.query("SELECT * FROM products"))
    print(db.query("SELECT * FROM users"))
    
    db.close()