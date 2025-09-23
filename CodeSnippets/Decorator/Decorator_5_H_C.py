from abc import ABC, abstractmethod
from functools import wraps
from typing import Any, Callable, Dict, List, Optional

class Component(ABC):
    @abstractmethod
    def execute(self) -> str:
        pass
    
    @abstractmethod
    def get_cost(self) -> float:
        pass

class BasicService(Component):
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
        self._metadata: Dict[str, Any] = {}
    
    def execute(self) -> str:
        return self._component.execute()
    
    def get_cost(self) -> float:
        return self._component.get_cost()
    
    def add_metadata(self, key: str, value: Any) -> None:
        self._metadata[key] = value
    
    def get_metadata(self) -> Dict[str, Any]:
        return self._metadata.copy()

class SecurityLayer(Enhancement):
    def __init__(self, component: Component, auth_level: str = "basic"):
        super().__init__(component)
        self._auth_level = auth_level
        self.add_metadata("security_level", auth_level)
    
    def execute(self) -> str:
        return f"[SECURED:{self._auth_level}] {super().execute()}"
    
    def get_cost(self) -> float:
        multiplier = {"basic": 1.2, "advanced": 1.5, "enterprise": 2.0}
        return super().get_cost() * multiplier.get(self._auth_level, 1.0)

class CacheLayer(Enhancement):
    _cache: Dict[str, str] = {}
    
    def __init__(self, component: Component, ttl_seconds: int = 300):
        super().__init__(component)
        self._ttl = ttl_seconds
        self._cache_key = f"{id(component)}_{hash(str(component))}"
        self.add_metadata("cache_ttl", ttl_seconds)
    
    def execute(self) -> str:
        if self._cache_key in self._cache:
            return f"[CACHED] {self._cache[self._cache_key]}"
        
        result = super().execute()
        self._cache[self._cache_key] = result
        return result
    
    def get_cost(self) -> float:
        return super().get_cost() + 2.0

class LoggingLayer(Enhancement):
    _execution_count = 0
    
    def __init__(self, component: Component, log_level: str = "INFO"):
        super().__init__(component)
        self._log_level = log_level
        self.add_metadata("log_level", log_level)
    
    def execute(self) -> str:
        LoggingLayer._execution_count += 1
        result = super().execute()
        return f"[LOG:{self._log_level}#{LoggingLayer._execution_count}] {result}"
    
    def get_cost(self) -> float:
        return super().get_cost() + 1.5

class ChainBuilder:
    def __init__(self, component: Component):
        self._component = component
    
    def with_security(self, level: str = "basic") -> 'ChainBuilder':
        self._component = SecurityLayer(self._component, level)
        return self
    
    def with_caching(self, ttl: int = 300) -> 'ChainBuilder':
        self._component = CacheLayer(self._component, ttl)
        return self
    
    def with_logging(self, level: str = "INFO") -> 'ChainBuilder':
        self._component = LoggingLayer(self._component, level)
        return self
    
    def build(self) -> Component:
        return self._component

if __name__ == "__main__":
    service = BasicService("DataProcessor", 15.0)
    
    enhanced_service = (ChainBuilder(service)
                       .with_security("enterprise")
                       .with_caching(600)
                       .with_logging("DEBUG")
                       .build())
    
    print("First execution:")
    print(f"Result: {enhanced_service.execute()}")
    print(f"Cost: ${enhanced_service.get_cost():.2f}")
    
    print("\nSecond execution (cached):")
    print(f"Result: {enhanced_service.execute()}")
    
    if isinstance(enhanced_service, Enhancement):
        print(f"Metadata: {enhanced_service.get_metadata()}")
    
    simple_service = SecurityLayer(CacheLayer(BasicService("SimpleAPI")), "advanced")
    print(f"\nSimple service: {simple_service.execute()}")
    print(f"Simple service cost: ${simple_service.get_cost():.2f}")