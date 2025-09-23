import logging
from typing import Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum

class ServiceStatus(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    ERROR = "error"

@dataclass
class ServiceResult:
    success: bool
    data: Any = None
    error: Optional[str] = None

class DatabaseService:
    def __init__(self):
        self._connected = False
        
    def connect(self) -> bool:
        self._connected = True
        return True
        
    def query(self, sql: str) -> ServiceResult:
        if not self._connected:
            return ServiceResult(False, error="Database not connected")
        return ServiceResult(True, data=f"Results for: {sql}")
        
    def disconnect(self):
        self._connected = False

class CacheService:
    def __init__(self):
        self._cache: Dict[str, Any] = {}
        
    def get(self, key: str) -> ServiceResult:
        if key in self._cache:
            return ServiceResult(True, data=self._cache[key])
        return ServiceResult(False, error="Key not found")
        
    def set(self, key: str, value: Any) -> ServiceResult:
        self._cache[key] = value
        return ServiceResult(True, data="Cached successfully")

class LoggingService:
    def __init__(self):
        self._logger = logging.getLogger(__name__)
        
    def log_info(self, message: str):
        self._logger.info(message)
        
    def log_error(self, message: str):
        self._logger.error(message)

class DataManager:
    def __init__(self):
        self._db = DatabaseService()
        self._cache = CacheService()
        self._logger = LoggingService()
        self._services_status = {}
        
    def initialize(self) -> bool:
        try:
            self._db.connect()
            self._services_status['database'] = ServiceStatus.ACTIVE
            self._services_status['cache'] = ServiceStatus.ACTIVE
            self._logger.log_info("DataManager initialized successfully")
            return True
        except Exception as e:
            self._logger.log_error(f"Initialization failed: {e}")
            return False
            
    def fetch_data(self, identifier: str, force_refresh: bool = False) -> ServiceResult:
        try:
            if not force_refresh:
                cached_result = self._cache.get(identifier)
                if cached_result.success:
                    self._logger.log_info(f"Data retrieved from cache: {identifier}")
                    return cached_result
                    
            db_result = self._db.query(f"SELECT * FROM data WHERE id = '{identifier}'")
            if db_result.success:
                self._cache.set(identifier, db_result.data)
                self._logger.log_info(f"Data retrieved from database: {identifier}")
                return db_result
            else:
                self._logger.log_error(f"Database query failed: {db_result.error}")
                return db_result
                
        except Exception as e:
            error_msg = f"Failed to fetch data for {identifier}: {e}"
            self._logger.log_error(error_msg)
            return ServiceResult(False, error=error_msg)
            
    def get_system_status(self) -> Dict[str, str]:
        return {service: status.value for service, status in self._services_status.items()}
        
    def shutdown(self):
        self._db.disconnect()
        self._services_status.clear()
        self._logger.log_info("DataManager shutdown completed")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    manager = DataManager()
    
    if manager.initialize():
        result1 = manager.fetch_data("user_123")
        print(f"First fetch: {result1}")
        
        result2 = manager.fetch_data("user_123")
        print(f"Second fetch (cached): {result2}")
        
        result3 = manager.fetch_data("user_123", force_refresh=True)
        print(f"Force refresh: {result3}")
        
        status = manager.get_system_status()
        print(f"System status: {status}")
        
        manager.shutdown()