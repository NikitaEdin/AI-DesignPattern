from abc import ABC, abstractmethod
import time
from typing import Dict, Any
import threading

class ResourceInterface(ABC):
    @abstractmethod
    def fetch_data(self, key: str) -> str:
        pass
    
    @abstractmethod
    def process_operation(self, operation: str, *args) -> Any:
        pass

class ExpensiveResource(ResourceInterface):
    def __init__(self):
        time.sleep(2)
        self.data = {
            'user_1': 'Alice Johnson',
            'user_2': 'Bob Smith',
            'user_3': 'Charlie Brown'
        }
    
    def fetch_data(self, key: str) -> str:
        time.sleep(1)
        return self.data.get(key, "Not found")
    
    def process_operation(self, operation: str, *args) -> Any:
        time.sleep(0.5)
        if operation == "count":
            return len(self.data)
        elif operation == "keys":
            return list(self.data.keys())
        elif operation == "add":
            if len(args) >= 2:
                self.data[args[0]] = args[1]
                return f"Added {args[0]}: {args[1]}"
        return "Invalid operation"

class CachingGateway(ResourceInterface):
    def __init__(self):
        self._resource = None
        self._cache: Dict[str, Any] = {}
        self._access_log: Dict[str, int] = {}
        self._lock = threading.Lock()
        self._max_cache_size = 10
    
    def _get_resource(self) -> ExpensiveResource:
        if self._resource is None:
            print("Initializing expensive resource...")
            self._resource = ExpensiveResource()
        return self._resource
    
    def _log_access(self, key: str):
        with self._lock:
            self._access_log[key] = self._access_log.get(key, 0) + 1
    
    def _manage_cache_size(self):
        if len(self._cache) >= self._max_cache_size:
            oldest_key = min(self._access_log.keys(), 
                           key=lambda k: self._access_log[k])
            del self._cache[oldest_key]
            del self._access_log[oldest_key]
    
    def fetch_data(self, key: str) -> str:
        cache_key = f"fetch_{key}"
        
        if cache_key in self._cache:
            self._log_access(cache_key)
            print(f"Cache hit for {key}")
            return self._cache[cache_key]
        
        print(f"Cache miss for {key}, fetching from resource...")
        result = self._get_resource().fetch_data(key)
        
        with self._lock:
            self._manage_cache_size()
            self._cache[cache_key] = result
            self._log_access(cache_key)
        
        return result
    
    def process_operation(self, operation: str, *args) -> Any:
        if operation in ["add"]:
            result = self._get_resource().process_operation(operation, *args)
            self._cache.clear()
            return result
        
        cache_key = f"op_{operation}_{hash(args)}"
        
        if cache_key in self._cache:
            self._log_access(cache_key)
            print(f"Cached operation result for {operation}")
            return self._cache[cache_key]
        
        print(f"Executing operation {operation}...")
        result = self._get_resource().process_operation(operation, *args)
        
        with self._lock:
            self._manage_cache_size()
            self._cache[cache_key] = result
            self._log_access(cache_key)
        
        return result
    
    def get_statistics(self) -> Dict[str, Any]:
        return {
            'cache_size': len(self._cache),
            'access_log': dict(self._access_log),
            'total_accesses': sum(self._access_log.values())
        }

if __name__ == "__main__":
    gateway = CachingGateway()
    
    print("=== First access (cache miss) ===")
    print(gateway.fetch_data("user_1"))
    
    print("\n=== Second access (cache hit) ===")
    print(gateway.fetch_data("user_1"))
    
    print("\n=== Operation caching ===")
    print(gateway.process_operation("count"))
    print(gateway.process_operation("count"))
    
    print("\n=== Cache invalidation ===")
    print(gateway.process_operation("add", "user_4", "Diana Prince"))
    print(gateway.process_operation("count"))
    
    print("\n=== Statistics ===")
    stats = gateway.get_statistics()
    for key, value in stats.items():
        print(f"{key}: {value}")