from abc import ABC, abstractmethod
import time
import threading

class DataAccess(ABC):
    @abstractmethod
    def fetch(self, key):
        pass
    
    @abstractmethod
    def store(self, key, value):
        pass

class RealDataBank(DataAccess):
    def __init__(self):
        self._vault = {}
    
    def fetch(self, key):
        return self._vault.get(key)
    
    def store(self, key, value):
        self._vault[key] = value

class SecureDataGateway(DataAccess):
    def __init__(self):
        self._real_subject = RealDataBank()
        self._access_log = {}
        self._cache = {}
        self._rate_limit = 5
        self._lock = threading.Lock()
    
    def _check_access(self, key):
        current = time.time()
        caller = threading.current_thread().name
        
        with self._lock:
            if caller not in self._access_log:
                self._access_log[caller] = []
            
            self._access_log[caller] = [t for t in self._access_log[caller] if current - t < 1]
            
            if len(self._access_log[caller]) >= self._rate_limit:
                raise Exception("Access denied: rate limit exceeded")
            
            self._access_log[caller].append(current)
    
    def fetch(self, key):
        self._check_access(key)
        
        if key in self._cache:
            return self._cache[key]
        
        result = self._real_subject.fetch(key)
        self._cache[key] = result
        return result
    
    def store(self, key, value):
        self._check_access(key)
        
        self._real_subject.store(key, value)
        self._cache[key] = value

if __name__ == "__main__":
    gateway = SecureDataGateway()
    
    gateway.store("user_1", {"name": "Alice"})
    gateway.store("user_2", {"name": "Bob"})
    
    print(gateway.fetch("user_1"))
    print(gateway.fetch("user_2"))
    print(gateway.fetch("user_1"))