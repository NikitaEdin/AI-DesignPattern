from typing import Dict, Any, Optional
import logging
from contextlib import contextmanager

class DatabaseManager:
    def __init__(self):
        self.connected = False
        self.transaction_active = False
    
    def connect(self):
        if not self.connected:
            self.connected = True
            return True
        return False
    
    def disconnect(self):
        if self.connected:
            self.connected = False
            return True
        return False
    
    def begin_transaction(self):
        if self.connected and not self.transaction_active:
            self.transaction_active = True
            return True
        return False
    
    def commit_transaction(self):
        if self.transaction_active:
            self.transaction_active = False
            return True
        return False
    
    def rollback_transaction(self):
        if self.transaction_active:
            self.transaction_active = False
            return True
        return False

class CacheService:
    def __init__(self):
        self.cache = {}
        self.enabled = False
    
    def enable(self):
        self.enabled = True
    
    def disable(self):
        self.enabled = False
    
    def get(self, key: str) -> Optional[Any]:
        return self.cache.get(key) if self.enabled else None
    
    def set(self, key: str, value: Any):
        if self.enabled:
            self.cache[key] = value
    
    def clear(self):
        self.cache.clear()

class LoggingService:
    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self.enabled = True
    
    def log_info(self, message: str):
        if self.enabled:
            self.logger.info(message)
    
    def log_error(self, message: str):
        if self.enabled:
            self.logger.error(message)
    
    def enable(self):
        self.enabled = True
    
    def disable(self):
        self.enabled = False

class DataProcessor:
    def __init__(self):
        self.db = DatabaseManager()
        self.cache = CacheService()
        self.logger = LoggingService()
    
    def initialize(self, enable_cache: bool = True, enable_logging: bool = True):
        if not self.db.connect():
            raise RuntimeError("Failed to connect to database")
        
        if enable_cache:
            self.cache.enable()
        if enable_logging:
            self.logger.enable()
        
        self.logger.log_info("System initialized successfully")
    
    def process_data(self, data_id: str, data: Dict[str, Any]) -> bool:
        try:
            cached_result = self.cache.get(data_id)
            if cached_result:
                self.logger.log_info(f"Using cached data for {data_id}")
                return True
            
            with self._transaction_context():
                self.logger.log_info(f"Processing data for {data_id}")
                processed_data = self._transform_data(data)
                self.cache.set(data_id, processed_data)
                return True
                
        except Exception as e:
            self.logger.log_error(f"Failed to process data {data_id}: {str(e)}")
            return False
    
    @contextmanager
    def _transaction_context(self):
        if not self.db.begin_transaction():
            raise RuntimeError("Failed to begin transaction")
        try:
            yield
            if not self.db.commit_transaction():
                raise RuntimeError("Failed to commit transaction")
        except Exception:
            self.db.rollback_transaction()
            raise
    
    def _transform_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return {k: str(v).upper() for k, v in data.items()}
    
    def shutdown(self):
        self.cache.clear()
        self.db.disconnect()
        self.logger.log_info("System shutdown complete")

if __name__ == "__main__":
    processor = DataProcessor()
    
    processor.initialize(enable_cache=True, enable_logging=True)
    
    test_data = {"name": "john", "email": "john@example.com", "age": 30}
    result = processor.process_data("user_001", test_data)
    print(f"First processing result: {result}")
    
    result = processor.process_data("user_001", test_data)
    print(f"Second processing result (cached): {result}")
    
    processor.shutdown()