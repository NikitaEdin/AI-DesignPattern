from abc import ABC, abstractmethod
from functools import wraps
import time

class Component(ABC):
    @abstractmethod
    def execute(self) -> str:
        pass
    
    @abstractmethod
    def get_cost(self) -> float:
        pass

class BaseService(Component):
    def __init__(self, name: str, base_cost: float = 10.0):
        self._name = name
        self._base_cost = base_cost
    
    def execute(self) -> str:
        return f"Executing {self._name}"
    
    def get_cost(self) -> float:
        return self._base_cost

class Enhancement(Component):
    def __init__(self, component: Component):
        self._component = component
        self._applied_at = time.time()
    
    @property
    def component(self) -> Component:
        return self._component
    
    def execute(self) -> str:
        return self._component.execute()
    
    def get_cost(self) -> float:
        return self._component.get_cost()

class SecurityWrapper(Enhancement):
    def __init__(self, component: Component, level: str = "standard"):
        super().__init__(component)
        self._security_level = level
        self._cost_multiplier = {"basic": 1.2, "standard": 1.5, "premium": 2.0}
    
    def execute(self) -> str:
        base_result = self._component.execute()
        return f"{base_result} -> Security({self._security_level}) applied"
    
    def get_cost(self) -> float:
        multiplier = self._cost_multiplier.get(self._security_level, 1.5)
        return self._component.get_cost() * multiplier

class CacheLayer(Enhancement):
    _cache = {}
    
    def __init__(self, component: Component, ttl: int = 300):
        super().__init__(component)
        self._ttl = ttl
        self._cache_key = f"{id(component)}_{hash(str(component))}"
    
    def execute(self) -> str:
        current_time = time.time()
        cache_entry = self._cache.get(self._cache_key)
        
        if cache_entry and (current_time - cache_entry['timestamp']) < self._ttl:
            return f"[CACHED] {cache_entry['result']}"
        
        result = self._component.execute()
        self._cache[self._cache_key] = {'result': result, 'timestamp': current_time}
        return result
    
    def get_cost(self) -> float:
        return self._component.get_cost() + 5.0

class LoggingWrapper(Enhancement):
    def __init__(self, component: Component, log_level: str = "INFO"):
        super().__init__(component)
        self._log_level = log_level
        self._execution_count = 0
    
    def execute(self) -> str:
        self._execution_count += 1
        start_time = time.time()
        result = self._component.execute()
        duration = (time.time() - start_time) * 1000
        
        log_entry = f"[{self._log_level}] Exec #{self._execution_count} | Duration: {duration:.2f}ms"
        return f"{result} | {log_entry}"
    
    def get_cost(self) -> float:
        return self._component.get_cost() + (self._execution_count * 0.1)

if __name__ == "__main__":
    base_service = BaseService("DataProcessor", 15.0)
    print(f"Base: {base_service.execute()}")
    print(f"Cost: ${base_service.get_cost():.2f}")
    
    secured_service = SecurityWrapper(base_service, "premium")
    print(f"\nSecured: {secured_service.execute()}")
    print(f"Cost: ${secured_service.get_cost():.2f}")
    
    cached_secured = CacheLayer(secured_service, ttl=60)
    print(f"\nCached: {cached_secured.execute()}")
    print(f"Cost: ${cached_secured.get_cost():.2f}")
    
    full_service = LoggingWrapper(cached_secured, "DEBUG")
    print(f"\nFull Stack:")
    for i in range(3):
        print(f"Run {i+1}: {full_service.execute()}")
    print(f"Final Cost: ${full_service.get_cost():.2f}")