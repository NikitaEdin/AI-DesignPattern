import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from contextlib import contextmanager

class DatabaseConnection:
    def __init__(self):
        self._connected = False
        self._transaction_active = False
    
    def connect(self):
        self._connected = True
        logging.info("Database connected")
    
    def disconnect(self):
        self._connected = False
        logging.info("Database disconnected")
    
    def execute_query(self, query: str):
        if not self._connected:
            raise RuntimeError("Database not connected")
        logging.info(f"Executing query: {query}")
        return f"Result for: {query}"
    
    def begin_transaction(self):
        self._transaction_active = True
        logging.info("Transaction started")
    
    def commit_transaction(self):
        self._transaction_active = False
        logging.info("Transaction committed")
    
    def rollback_transaction(self):
        self._transaction_active = False
        logging.info("Transaction rolled back")

class CacheService:
    def __init__(self):
        self._cache: Dict[str, Any] = {}
        self._enabled = False
    
    def enable(self):
        self._enabled = True
        logging.info("Cache enabled")
    
    def disable(self):
        self._enabled = False
        logging.info("Cache disabled")
    
    def get(self, key: str) -> Optional[Any]:
        if self._enabled and key in self._cache:
            logging.info(f"Cache hit for key: {key}")
            return self._cache[key]
        return None
    
    def set(self, key: str, value: Any):
        if self._enabled:
            self._cache[key] = value
            logging.info(f"Cache set for key: {key}")

class SecurityValidator:
    def __init__(self):
        self._authorized_users = set()
    
    def authenticate(self, user_id: str, password: str) -> bool:
        if user_id == "admin" and password == "secret":
            self._authorized_users.add(user_id)
            logging.info(f"User {user_id} authenticated")
            return True
        logging.warning(f"Authentication failed for {user_id}")
        return False
    
    def is_authorized(self, user_id: str) -> bool:
        return user_id in self._authorized_users

class DataManager:
    def __init__(self):
        self._db = DatabaseConnection()
        self._cache = CacheService()
        self._security = SecurityValidator()
        self._current_user: Optional[str] = None
    
    def initialize(self):
        self._db.connect()
        self._cache.enable()
        logging.info("Data manager initialized")
    
    def shutdown(self):
        self._db.disconnect()
        self._cache.disable()
        logging.info("Data manager shutdown")
    
    def login(self, user_id: str, password: str) -> bool:
        if self._security.authenticate(user_id, password):
            self._current_user = user_id
            return True
        return False
    
    @contextmanager
    def transaction_scope(self):
        if not self._current_user or not self._security.is_authorized(self._current_user):
            raise PermissionError("Unauthorized access")
        
        self._db.begin_transaction()
        try:
            yield
            self._db.commit_transaction()
        except Exception as e:
            self._db.rollback_transaction()
            logging.error(f"Transaction failed: {e}")
            raise
    
    def fetch_data(self, query: str) -> str:
        if not self._current_user or not self._security.is_authorized(self._current_user):
            raise PermissionError("Unauthorized access")
        
        cached_result = self._cache.get(query)
        if cached_result:
            return cached_result
        
        result = self._db.execute_query(query)
        self._cache.set(query, result)
        return result

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    
    manager = DataManager()
    manager.initialize()
    
    try:
        if manager.login("admin", "secret"):
            with manager.transaction_scope():
                data1 = manager.fetch_data("SELECT * FROM users")
                data2 = manager.fetch_data("SELECT * FROM users")
                print(f"Fetched: {data1}")
                print(f"Cached: {data2}")
    except PermissionError as e:
        print(f"Error: {e}")
    finally:
        manager.shutdown()