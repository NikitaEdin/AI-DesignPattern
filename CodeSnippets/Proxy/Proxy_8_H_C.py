import time
import threading
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from functools import wraps

class DatabaseInterface(ABC):
    @abstractmethod
    def query(self, sql: str) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    def connect(self) -> bool:
        pass
    
    @abstractmethod
    def disconnect(self) -> bool:
        pass

class RealDatabase(DatabaseInterface):
    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self.connected = False
        self._data = {
            "users": [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}],
            "products": [{"id": 1, "name": "Laptop"}, {"id": 2, "name": "Mouse"}]
        }
    
    def connect(self) -> bool:
        time.sleep(0.5)
        self.connected = True
        return True
    
    def disconnect(self) -> bool:
        self.connected = False
        return True
    
    def query(self, sql: str) -> Dict[str, Any]:
        if not self.connected:
            raise ConnectionError("Database not connected")
        
        time.sleep(0.2)
        table = sql.split("FROM")[1].strip().split()[0]
        return {"data": self._data.get(table, []), "status": "success"}

class DatabaseGuard(DatabaseInterface):
    def __init__(self, connection_string: str, user_role: str = "user"):
        self._real_db = None
        self._connection_string = connection_string
        self._user_role = user_role
        self._cache: Dict[str, tuple] = {}
        self._cache_timeout = 5
        self._lock = threading.RLock()
        self._connection_pool = []
        self._max_connections = 3
    
    def _authenticate(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if self._user_role not in ["admin", "user"]:
                raise PermissionError("Unauthorized access")
            return func(self, *args, **kwargs)
        return wrapper
    
    def _get_cached_result(self, key: str) -> Optional[Dict[str, Any]]:
        if key in self._cache:
            result, timestamp = self._cache[key]
            if time.time() - timestamp < self._cache_timeout:
                return result
            else:
                del self._cache[key]
        return None
    
    def _cache_result(self, key: str, result: Dict[str, Any]) -> None:
        self._cache[key] = (result, time.time())
    
    def _get_connection(self) -> RealDatabase:
        with self._lock:
            if len(self._connection_pool) < self._max_connections:
                db = RealDatabase(self._connection_string)
                db.connect()
                self._connection_pool.append(db)
                return db
            return self._connection_pool[0]
    
    @_authenticate
    def connect(self) -> bool:
        self._real_db = self._get_connection()
        return True
    
    @_authenticate
    def disconnect(self) -> bool:
        if self._real_db:
            return self._real_db.disconnect()
        return True
    
    @_authenticate
    def query(self, sql: str) -> Dict[str, Any]:
        if "DROP" in sql.upper() or "DELETE" in sql.upper():
            if self._user_role != "admin":
                raise PermissionError("Insufficient privileges for destructive operations")
        
        cached_result = self._get_cached_result(sql)
        if cached_result:
            cached_result["cached"] = True
            return cached_result
        
        if not self._real_db:
            self.connect()
        
        result = self._real_db.query(sql)
        self._cache_result(sql, result.copy())
        result["cached"] = False
        return result

if __name__ == "__main__":
    guard = DatabaseGuard("localhost:5432", "user")
    
    print("First query (cache miss):")
    result1 = guard.query("SELECT * FROM users")
    print(f"Result: {result1}")
    
    print("\nSecond query (cache hit):")
    result2 = guard.query("SELECT * FROM users")
    print(f"Result: {result2}")
    
    try:
        print("\nAttempting destructive operation:")
        guard.query("DELETE FROM users")
    except PermissionError as e:
        print(f"Access denied: {e}")
    
    admin_guard = DatabaseGuard("localhost:5432", "admin")
    print("\nAdmin destructive operation:")
    result3 = admin_guard.query("DELETE FROM users")
    print(f"Result: {result3}")
    
    guard.disconnect()
    admin_guard.disconnect()