import logging
from typing import Dict, Any, Optional
from abc import ABC, abstractmethod

class DatabaseConnection:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.connected = False
    
    def connect(self):
        if not self.connected:
            self.connected = True
            return f"Connected to database at {self.host}:{self.port}"
        return "Already connected"
    
    def execute_query(self, query: str):
        if not self.connected:
            raise ConnectionError("Database not connected")
        return f"Executed: {query}"
    
    def disconnect(self):
        if self.connected:
            self.connected = False
            return "Disconnected from database"
        return "Already disconnected"

class CacheService:
    def __init__(self):
        self.cache = {}
        self.enabled = False
    
    def enable(self):
        self.enabled = True
        return "Cache service enabled"
    
    def get(self, key: str):
        if not self.enabled:
            return None
        return self.cache.get(key)
    
    def set(self, key: str, value: Any):
        if self.enabled:
            self.cache[key] = value
    
    def clear(self):
        self.cache.clear()
        return "Cache cleared"

class LoggingService:
    def __init__(self, level: str = "INFO"):
        logging.basicConfig(level=getattr(logging, level.upper()))
        self.logger = logging.getLogger(__name__)
    
    def log_info(self, message: str):
        self.logger.info(message)
    
    def log_error(self, message: str):
        self.logger.error(message)
    
    def log_debug(self, message: str):
        self.logger.debug(message)

class DataAccessManager:
    def __init__(self, db_host: str = "localhost", db_port: int = 5432):
        self.database = DatabaseConnection(db_host, db_port)
        self.cache = CacheService()
        self.logger = LoggingService()
        self._initialized = False
    
    def initialize(self):
        if self._initialized:
            return "System already initialized"
        
        try:
            self.database.connect()
            self.cache.enable()
            self.logger.log_info("Data access system initialized successfully")
            self._initialized = True
            return "System initialized successfully"
        except Exception as e:
            self.logger.log_error(f"Failed to initialize system: {str(e)}")
            raise
    
    def fetch_user_data(self, user_id: int) -> Optional[Dict[str, Any]]:
        if not self._initialized:
            raise RuntimeError("System not initialized")
        
        cache_key = f"user_{user_id}"
        cached_data = self.cache.get(cache_key)
        
        if cached_data:
            self.logger.log_info(f"Retrieved user {user_id} from cache")
            return cached_data
        
        try:
            query = f"SELECT * FROM users WHERE id = {user_id}"
            result = self.database.execute_query(query)
            
            user_data = {"id": user_id, "name": f"User{user_id}", "email": f"user{user_id}@example.com"}
            self.cache.set(cache_key, user_data)
            
            self.logger.log_info(f"Retrieved and cached user {user_id} from database")
            return user_data
        
        except Exception as e:
            self.logger.log_error(f"Failed to fetch user {user_id}: {str(e)}")
            return None
    
    def update_user_data(self, user_id: int, data: Dict[str, Any]) -> bool:
        if not self._initialized:
            raise RuntimeError("System not initialized")
        
        try:
            query = f"UPDATE users SET name='{data.get('name')}' WHERE id = {user_id}"
            self.database.execute_query(query)
            
            cache_key = f"user_{user_id}"
            self.cache.set(cache_key, data)
            
            self.logger.log_info(f"Updated user {user_id} data")
            return True
        
        except Exception as e:
            self.logger.log_error(f"Failed to update user {user_id}: {str(e)}")
            return False
    
    def clear_cache(self):
        self.cache.clear()
        self.logger.log_info("System cache cleared")
    
    def shutdown(self):
        if self._initialized:
            self.database.disconnect()
            self.cache.clear()
            self.logger.log_info("Data access system shut down")
            self._initialized = False

if __name__ == "__main__":
    manager = DataAccessManager("production.db.com", 5432)
    
    manager.initialize()
    
    user_data = manager.fetch_user_data(123)
    print(f"Fetched data: {user_data}")
    
    user_data = manager.fetch_user_data(123)
    print(f"Cached data: {user_data}")
    
    success = manager.update_user_data(123, {"name": "John Doe", "email": "john@example.com"})
    print(f"Update successful: {success}")
    
    manager.clear_cache()
    manager.shutdown()