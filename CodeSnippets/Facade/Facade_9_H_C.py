import logging
from typing import Dict, Any, Optional
from contextlib import contextmanager

class DatabaseConnection:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.connected = False
    
    def connect(self):
        if not self.connected:
            self.connected = True
            return True
        return False
    
    def disconnect(self):
        self.connected = False
    
    def execute_query(self, query: str) -> Dict[str, Any]:
        if not self.connected:
            raise ConnectionError("Database not connected")
        return {"result": f"Query '{query}' executed", "rows": 5}

class CacheService:
    def __init__(self):
        self.cache = {}
        self.enabled = False
    
    def enable(self):
        self.enabled = True
    
    def get(self, key: str) -> Optional[Any]:
        return self.cache.get(key) if self.enabled else None
    
    def set(self, key: str, value: Any):
        if self.enabled:
            self.cache[key] = value
    
    def clear(self):
        self.cache.clear()

class SecurityManager:
    def __init__(self):
        self.authenticated_users = set()
    
    def authenticate(self, user_id: str, token: str) -> bool:
        if len(token) >= 10:
            self.authenticated_users.add(user_id)
            return True
        return False
    
    def is_authorized(self, user_id: str, resource: str) -> bool:
        return user_id in self.authenticated_users

class LoggingService:
    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def log_access(self, user_id: str, action: str):
        self.logger.info(f"User {user_id} performed: {action}")
    
    def log_error(self, error: str):
        self.logger.error(f"Error occurred: {error}")

class DataAccessManager:
    def __init__(self):
        self.db = DatabaseConnection("localhost", 5432)
        self.cache = CacheService()
        self.security = SecurityManager()
        self.logger = LoggingService()
        self._initialized = False
    
    @contextmanager
    def session(self, user_id: str, auth_token: str):
        if not self._initialized:
            self._initialize_system()
        
        if not self.security.authenticate(user_id, auth_token):
            raise PermissionError("Authentication failed")
        
        try:
            yield self
        finally:
            self.logger.log_access(user_id, "session_ended")
    
    def _initialize_system(self):
        self.db.connect()
        self.cache.enable()
        self._initialized = True
    
    def fetch_data(self, user_id: str, query: str) -> Dict[str, Any]:
        if not self.security.is_authorized(user_id, "data_read"):
            raise PermissionError("User not authorized")
        
        cache_key = f"query_{hash(query)}"
        cached_result = self.cache.get(cache_key)
        
        if cached_result:
            self.logger.log_access(user_id, f"cache_hit: {query[:30]}...")
            return cached_result
        
        try:
            result = self.db.execute_query(query)
            self.cache.set(cache_key, result)
            self.logger.log_access(user_id, f"db_query: {query[:30]}...")
            return result
        except Exception as e:
            self.logger.log_error(str(e))
            raise
    
    def update_data(self, user_id: str, query: str) -> bool:
        if not self.security.is_authorized(user_id, "data_write"):
            raise PermissionError("User not authorized for updates")
        
        try:
            self.db.execute_query(query)
            self.cache.clear()
            self.logger.log_access(user_id, f"data_updated: {query[:30]}...")
            return True
        except Exception as e:
            self.logger.log_error(str(e))
            return False

if __name__ == "__main__":
    manager = DataAccessManager()
    
    try:
        with manager.session("user123", "valid_token_123") as session:
            result = session.fetch_data("user123", "SELECT * FROM users")
            print(f"Data retrieved: {result}")
            
            cached_result = session.fetch_data("user123", "SELECT * FROM users")
            print(f"Cached data: {cached_result}")
            
            update_success = session.update_data("user123", "UPDATE users SET status='active'")
            print(f"Update successful: {update_success}")
    
    except PermissionError as e:
        print(f"Access denied: {e}")
    except Exception as e:
        print(f"Operation failed: {e}")