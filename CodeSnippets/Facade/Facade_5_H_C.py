import logging
from typing import Dict, Any, Optional
from dataclasses import dataclass
from contextlib import contextmanager

@dataclass
class ProcessResult:
    success: bool
    data: Any = None
    error: str = ""

class DatabaseConnection:
    def __init__(self):
        self._connected = False
        self._data = {"users": [], "products": [], "orders": []}
    
    def connect(self):
        self._connected = True
        return self._connected
    
    def disconnect(self):
        self._connected = False
    
    def query(self, table: str, filters: Dict = None):
        if not self._connected:
            raise ConnectionError("Database not connected")
        return self._data.get(table, [])
    
    def insert(self, table: str, data: Dict):
        if not self._connected:
            raise ConnectionError("Database not connected")
        if table in self._data:
            self._data[table].append(data)

class CacheManager:
    def __init__(self):
        self._cache = {}
        self._enabled = True
    
    def get(self, key: str):
        return self._cache.get(key) if self._enabled else None
    
    def set(self, key: str, value: Any):
        if self._enabled:
            self._cache[key] = value
    
    def invalidate(self, pattern: str = None):
        if pattern:
            keys_to_remove = [k for k in self._cache if pattern in k]
            for key in keys_to_remove:
                del self._cache[key]
        else:
            self._cache.clear()

class ValidationService:
    def validate_user(self, user_data: Dict) -> bool:
        required_fields = ['name', 'email']
        return all(field in user_data for field in required_fields)
    
    def validate_product(self, product_data: Dict) -> bool:
        required_fields = ['name', 'price']
        return all(field in product_data for field in required_fields)

class ECommerceSystem:
    def __init__(self):
        self._db = DatabaseConnection()
        self._cache = CacheManager()
        self._validator = ValidationService()
        self._logger = logging.getLogger(__name__)
    
    @contextmanager
    def _database_session(self):
        try:
            self._db.connect()
            yield self._db
        except Exception as e:
            self._logger.error(f"Database operation failed: {e}")
            raise
        finally:
            self._db.disconnect()
    
    def create_user(self, user_data: Dict) -> ProcessResult:
        try:
            if not self._validator.validate_user(user_data):
                return ProcessResult(False, error="Invalid user data")
            
            with self._database_session() as db:
                db.insert('users', user_data)
                self._cache.invalidate('users')
                return ProcessResult(True, user_data)
        except Exception as e:
            return ProcessResult(False, error=str(e))
    
    def get_users(self, use_cache: bool = True) -> ProcessResult:
        try:
            cache_key = 'users_list'
            if use_cache:
                cached_result = self._cache.get(cache_key)
                if cached_result:
                    return ProcessResult(True, cached_result)
            
            with self._database_session() as db:
                users = db.query('users')
                self._cache.set(cache_key, users)
                return ProcessResult(True, users)
        except Exception as e:
            return ProcessResult(False, error=str(e))
    
    def add_product(self, product_data: Dict) -> ProcessResult:
        try:
            if not self._validator.validate_product(product_data):
                return ProcessResult(False, error="Invalid product data")
            
            with self._database_session() as db:
                db.insert('products', product_data)
                self._cache.invalidate('products')
                return ProcessResult(True, product_data)
        except Exception as e:
            return ProcessResult(False, error=str(e))

if __name__ == "__main__":
    system = ECommerceSystem()
    
    user_result = system.create_user({"name": "John Doe", "email": "john@example.com"})
    print(f"User creation: {user_result}")
    
    users_result = system.get_users()
    print(f"Users list: {users_result}")
    
    product_result = system.add_product({"name": "Laptop", "price": 999.99})
    print(f"Product addition: {product_result}")
    
    invalid_user = system.create_user({"name": "Jane"})
    print(f"Invalid user creation: {invalid_user}")