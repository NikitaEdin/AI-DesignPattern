from typing import Dict, Any, Optional, List
import json
import hashlib
import time

class DatabaseManager:
    def __init__(self):
        self._connection_pool = {}
        self._query_cache = {}
    
    def connect(self, db_name: str) -> bool:
        if db_name not in self._connection_pool:
            self._connection_pool[db_name] = f"connection_{db_name}"
            return True
        return False
    
    def execute_query(self, db_name: str, query: str) -> List[Dict]:
        if db_name not in self._connection_pool:
            raise ConnectionError(f"No connection to {db_name}")
        
        cache_key = hashlib.md5(f"{db_name}_{query}".encode()).hexdigest()
        if cache_key in self._query_cache:
            return self._query_cache[cache_key]
        
        result = [{"id": 1, "data": f"result_for_{query}"}]
        self._query_cache[cache_key] = result
        return result

class CacheService:
    def __init__(self):
        self._cache = {}
        self._ttl = {}
    
    def get(self, key: str) -> Optional[Any]:
        if key in self._cache:
            if time.time() < self._ttl.get(key, 0):
                return self._cache[key]
            else:
                self.invalidate(key)
        return None
    
    def set(self, key: str, value: Any, ttl: int = 300):
        self._cache[key] = value
        self._ttl[key] = time.time() + ttl
    
    def invalidate(self, key: str):
        self._cache.pop(key, None)
        self._ttl.pop(key, None)

class AuthenticationService:
    def __init__(self):
        self._sessions = {}
        self._users = {"admin": "password123", "user": "pass456"}
    
    def authenticate(self, username: str, password: str) -> Optional[str]:
        if self._users.get(username) == password:
            session_id = hashlib.md5(f"{username}_{time.time()}".encode()).hexdigest()
            self._sessions[session_id] = {"username": username, "expires": time.time() + 3600}
            return session_id
        return None
    
    def validate_session(self, session_id: str) -> bool:
        session = self._sessions.get(session_id)
        if session and time.time() < session["expires"]:
            return True
        if session_id in self._sessions:
            del self._sessions[session_id]
        return False

class DataProcessor:
    @staticmethod
    def transform(data: List[Dict], format_type: str = "json") -> str:
        if format_type == "json":
            return json.dumps(data, indent=2)
        elif format_type == "csv":
            if not data:
                return ""
            headers = ",".join(data[0].keys())
            rows = "\n".join([",".join(str(v) for v in row.values()) for row in data])
            return f"{headers}\n{rows}"
        return str(data)

class BusinessOperationsManager:
    def __init__(self):
        self._db = DatabaseManager()
        self._cache = CacheService()
        self._auth = AuthenticationService()
        self._processor = DataProcessor()
        self._active_sessions = set()
    
    def login_and_fetch_data(self, username: str, password: str, query: str, db_name: str = "main", format_type: str = "json") -> Dict[str, Any]:
        try:
            session_id = self._auth.authenticate(username, password)
            if not session_id:
                return {"success": False, "error": "Authentication failed"}
            
            self._active_sessions.add(session_id)
            
            cache_key = f"{db_name}_{query}_{format_type}"
            cached_result = self._cache.get(cache_key)
            
            if cached_result:
                return {
                    "success": True,
                    "session_id": session_id,
                    "data": cached_result,
                    "source": "cache"
                }
            
            self._db.connect(db_name)
            raw_data = self._db.execute_query(db_name, query)
            processed_data = self._processor.transform(raw_data, format_type)
            
            self._cache.set(cache_key, processed_data)
            
            return {
                "success": True,
                "session_id": session_id,
                "data": processed_data,
                "source": "database"
            }
        
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def execute_authenticated_operation(self, session_id: str, operation: str, **kwargs) -> Dict[str, Any]:
        if not self._auth.validate_session(session_id):
            return {"success": False, "error": "Invalid or expired session"}
        
        if operation == "query":
            db_name = kwargs.get("db_name", "main")
            query = kwargs.get("query", "")
            format_type = kwargs.get("format", "json")
            
            try:
                self._db.connect(db_name)
                raw_data = self._db.execute_query(db_name, query)
                processed_data = self._processor.transform(raw_data, format_type)
                return {"success": True, "data": processed_data}
            except Exception as e:
                return {"success": False, "error": str(e)}
        
        return {"success": False, "error": "Unknown operation"}
    
    def logout(self, session_id: str) -> bool:
        self._active_sessions.discard(session_id)
        return True

if __name__ == "__main__":
    manager = BusinessOperationsManager()
    
    result = manager.login_and_fetch_data("admin", "password123", "SELECT * FROM users", "main", "json")
    print("Login and fetch result:", result)
    
    if result["success"]:
        session_id = result["session_id"]
        
        query_result = manager.execute_authenticated_operation(
            session_id, "query", 
            db_name="analytics", 
            query="SELECT COUNT(*) FROM orders", 
            format="csv"
        )
        print("Authenticated query result:", query_result)
        
        manager.logout(session_id)
        print("Logged out successfully")