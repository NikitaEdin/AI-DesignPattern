import logging
from typing import Dict, Any, Optional
from contextlib import contextmanager

class DatabaseManager:
    def __init__(self):
        self._connected = False
        self._transaction_active = False
    
    def connect(self):
        if not self._connected:
            self._connected = True
            logging.info("Database connected")
    
    def disconnect(self):
        if self._connected:
            self._connected = False
            logging.info("Database disconnected")
    
    def begin_transaction(self):
        if self._connected and not self._transaction_active:
            self._transaction_active = True
            logging.info("Transaction started")
    
    def commit(self):
        if self._transaction_active:
            self._transaction_active = False
            logging.info("Transaction committed")
    
    def rollback(self):
        if self._transaction_active:
            self._transaction_active = False
            logging.info("Transaction rolled back")

class CacheService:
    def __init__(self):
        self._cache = {}
        self._enabled = False
    
    def enable(self):
        self._enabled = True
        logging.info("Cache enabled")
    
    def get(self, key: str) -> Optional[Any]:
        if self._enabled:
            return self._cache.get(key)
        return None
    
    def set(self, key: str, value: Any):
        if self._enabled:
            self._cache[key] = value
            logging.info(f"Cached: {key}")
    
    def clear(self):
        self._cache.clear()
        logging.info("Cache cleared")

class ValidationService:
    def __init__(self):
        self._rules = {}
    
    def add_rule(self, field: str, rule_func):
        self._rules[field] = rule_func
    
    def validate(self, data: Dict[str, Any]) -> bool:
        for field, rule in self._rules.items():
            if field in data and not rule(data[field]):
                logging.error(f"Validation failed for field: {field}")
                return False
        return True

class DataProcessor:
    def __init__(self):
        self._db = DatabaseManager()
        self._cache = CacheService()
        self._validator = ValidationService()
        self._setup_validation_rules()
    
    def _setup_validation_rules(self):
        self._validator.add_rule('email', lambda x: '@' in str(x))
        self._validator.add_rule('age', lambda x: isinstance(x, int) and 0 <= x <= 150)
    
    @contextmanager
    def _database_transaction(self):
        self._db.connect()
        self._db.begin_transaction()
        try:
            yield
            self._db.commit()
        except Exception:
            self._db.rollback()
            raise
        finally:
            self._db.disconnect()
    
    def save_user_data(self, user_id: str, data: Dict[str, Any]) -> bool:
        try:
            cached_data = self._cache.get(user_id)
            if cached_data == data:
                logging.info(f"Data unchanged for user {user_id}")
                return True
            
            if not self._validator.validate(data):
                return False
            
            with self._database_transaction():
                logging.info(f"Saving user data for {user_id}")
                self._cache.set(user_id, data)
                return True
                
        except Exception as e:
            logging.error(f"Failed to save user data: {e}")
            return False
    
    def initialize_system(self):
        self._cache.enable()
        logging.info("System initialized successfully")
    
    def cleanup_system(self):
        self._cache.clear()
        logging.info("System cleanup completed")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    
    processor = DataProcessor()
    processor.initialize_system()
    
    user_data = {
        'name': 'John Doe',
        'email': 'john@example.com',
        'age': 30
    }
    
    success = processor.save_user_data('user123', user_data)
    print(f"Save operation successful: {success}")
    
    success = processor.save_user_data('user123', user_data)
    print(f"Second save operation successful: {success}")
    
    invalid_data = {'name': 'Jane', 'email': 'invalid-email', 'age': 200}
    success = processor.save_user_data('user456', invalid_data)
    print(f"Invalid data save successful: {success}")
    
    processor.cleanup_system()