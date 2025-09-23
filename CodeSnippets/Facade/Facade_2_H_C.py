from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import json

@dataclass
class ProcessResult:
    success: bool
    data: Any
    errors: List[str]

class DatabaseManager:
    def __init__(self):
        self._connection = None
        self._transactions = []
    
    def connect(self) -> bool:
        self._connection = "db_connection_active"
        return True
    
    def execute_query(self, query: str) -> Dict:
        if not self._connection:
            raise ConnectionError("No database connection")
        return {"query": query, "result": f"executed_{len(query)}_chars"}
    
    def start_transaction(self):
        self._transactions.append("transaction_started")
    
    def commit(self):
        if self._transactions:
            self._transactions.pop()

class CacheService:
    def __init__(self):
        self._cache = {}
        self._ttl = {}
    
    def get(self, key: str) -> Optional[Any]:
        return self._cache.get(key)
    
    def set(self, key: str, value: Any, ttl: int = 300):
        self._cache[key] = value
        self._ttl[key] = ttl
    
    def invalidate(self, pattern: str):
        keys_to_remove = [k for k in self._cache if pattern in k]
        for key in keys_to_remove:
            del self._cache[key]

class LoggingService:
    def __init__(self):
        self._logs = []
    
    def log_info(self, message: str):
        self._logs.append(f"INFO: {message}")
    
    def log_error(self, message: str):
        self._logs.append(f"ERROR: {message}")
    
    def get_logs(self) -> List[str]:
        return self._logs[-10:]

class ValidationService:
    @staticmethod
    def validate_data(data: Dict) -> List[str]:
        errors = []
        if not data:
            errors.append("Data cannot be empty")
        if "id" not in data:
            errors.append("ID field is required")
        return errors

class UnifiedDataProcessor:
    def __init__(self):
        self._db = DatabaseManager()
        self._cache = CacheService()
        self._logger = LoggingService()
        self._validator = ValidationService()
        self._initialized = False
    
    def initialize(self) -> bool:
        try:
            self._db.connect()
            self._logger.log_info("System initialized successfully")
            self._initialized = True
            return True
        except Exception as e:
            self._logger.log_error(f"Initialization failed: {str(e)}")
            return False
    
    def process_user_data(self, user_data: Dict) -> ProcessResult:
        if not self._initialized:
            return ProcessResult(False, None, ["System not initialized"])
        
        errors = self._validator.validate_data(user_data)
        if errors:
            self._logger.log_error(f"Validation failed: {errors}")
            return ProcessResult(False, None, errors)
        
        cache_key = f"user_{user_data['id']}"
        cached_result = self._cache.get(cache_key)
        
        if cached_result:
            self._logger.log_info(f"Retrieved user {user_data['id']} from cache")
            return ProcessResult(True, cached_result, [])
        
        try:
            self._db.start_transaction()
            query_result = self._db.execute_query(f"SELECT * FROM users WHERE id = {user_data['id']}")
            processed_data = {**user_data, **query_result, "processed": True}
            
            self._cache.set(cache_key, processed_data, ttl=600)
            self._db.commit()
            
            self._logger.log_info(f"Successfully processed user {user_data['id']}")
            return ProcessResult(True, processed_data, [])
            
        except Exception as e:
            error_msg = f"Processing failed: {str(e)}"
            self._logger.log_error(error_msg)
            return ProcessResult(False, None, [error_msg])
    
    def bulk_process(self, data_list: List[Dict]) -> Dict[str, Any]:
        results = {"successful": 0, "failed": 0, "details": []}
        
        for data in data_list:
            result = self.process_user_data(data)
            if result.success:
                results["successful"] += 1
            else:
                results["failed"] += 1
            results["details"].append({"data_id": data.get("id", "unknown"), "success": result.success})
        
        return results
    
    def get_system_status(self) -> Dict[str, Any]:
        return {
            "initialized": self._initialized,
            "recent_logs": self._logger.get_logs(),
            "cache_size": len(self._cache._cache)
        }

if __name__ == "__main__":
    processor = UnifiedDataProcessor()
    
    if processor.initialize():
        test_data = [
            {"id": 1, "name": "Alice", "email": "alice@example.com"},
            {"id": 2, "name": "Bob", "email": "bob@example.com"},
            {"name": "Charlie"}
        ]
        
        single_result = processor.process_user_data(test_data[0])
        print(f"Single process result: {single_result.success}")
        
        bulk_results = processor.bulk_process(test_data)
        print(f"Bulk processing: {bulk_results['successful']} succeeded, {bulk_results['failed']} failed")
        
        status = processor.get_system_status()
        print(f"System status: {json.dumps(status, indent=2)}")