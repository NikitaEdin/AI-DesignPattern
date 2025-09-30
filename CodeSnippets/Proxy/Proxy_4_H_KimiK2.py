from abc import ABC, abstractmethod
import threading
import weakref
import time
from typing import Optional

class DataAccess(ABC):
    @abstractmethod
    def fetch_data(self, key: str) -> str:
        pass

class RealDataService(DataAccess):
    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self._initialize_connection()
    
    def _initialize_connection(self):
        pass
    
    def fetch_data(self, SecureKey: str) -> str:
        time.sleep(0.1)
        return f"Data[{SecureKey}]"

class SecureAccessWrapper(DataAccess):
    _instances = weakref.WeakValueDictionary()
    _lock = threading.RLock()
    _ref_count = {}
    
    def __new__(cls, service: DataAccess):
        with cls._lock:
            instance_key = id(service)
            if instance_key in cls._instances:
                cls._ref_count[instance_key] += 1
                return cls._instances[instance_key]
            instance = super().__new__(cls)
            cls._instances[instance_key] = instance
            cls._ref_count[instance_key] = 1
            return instance
    
    def __init__(self, service: DataAccess):
        if hasattr(self, '_initialized'):
            return
        self._service = service
        self._cache = {}
        self._cache_lock = threading.RLock()
        self._access_log = []
        self._log_lock = threading.Lock()
        self._initialized = True
    
    def fetch_data(self, key: str) -> str:
        if not self._check_access(key):
            raise PermissionError("Access denied")
        
        with self._cache_lock:
            if key in self._cache:
                return self._cache[key]
        
        data = self._service.fetch_data(key)
        
        with self._cache_lock:
            self._cache[key] = data
        
        with self._log_lock:
            self._access_log.append((time.time(), key, threading.current_thread().name))
        
        return data
    
    def _check_access(self, key: str) -> bool:
        return not key.startswith("restricted_")
    
    def __del__(self):
        with self._lock:
            instance_key = id(self._service)
            self._ref_count[instance_key] -= 1
            if self._ref_count[instance_key] == 0:
                del self._instances[instance_key]
                del self._ref_count[instance_key]

class UsageTracker(DataAccess):
    def __init__(self, wrapped_service: DataAccess):
        self._wrapped = wrapped_service
        self._call_count = 0
        self._total_time = 0.0
        self._lock = threading.Lock()
    
    def fetch_data(self, key: str) -> str:
        start_time = time.time()
        self._call_count += 1
        
        try:
            result = self._wrapped.fetch_data(key)
            return result
        finally:
            elapsed = time.time() - start_time
            self._total_time += elapsed
    
    def get_stats(self) -> dict:
        with self._lock:
            avg_time = self._total_time / self._call_count if self._call_count > 0 else 0.0
            return {"calls": self._call_count, "avg_time": avg_time}

if __name__ == "__main__":
    real_service = RealDataService("server:1234")
    secure_access = SecureAccessWrapper(real_service)
    monitored_access = UsageTracker(secure_access)
    
    try:
        data1 = monitored_access.fetch_data("item1")
        data2 = monitored_access.fetch_data("restricted_item")
    except PermissionError:
        pass
    
    stats = monitored_access.get_stats()
    print(f"Calls: {stats['calls']}, Avg time: {stats['avg_time']:.4f}s")