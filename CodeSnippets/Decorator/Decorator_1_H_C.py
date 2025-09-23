from abc import ABC, abstractmethod
from functools import wraps
from typing import Any, Dict, Optional

class Component(ABC):
    @abstractmethod
    def execute(self) -> str:
        pass
    
    @abstractmethod
    def get_cost(self) -> float:
        pass

class BaseService(Component):
    def __init__(self, name: str, base_cost: float):
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
    
    def get_metadata(self, key: str) -> Optional[Any]:
        return self._metadata.get(key)

class SecurityWrapper(Enhancement):
    def __init__(self, component: Component, security_level: int = 1):
        super().__init__(component)
        self._security_level = security_level
        self.add_metadata("security_enabled", True)
        self.add_metadata("security_level", security_level)
    
    def execute(self) -> str:
        result = super().execute()
        return f"[SECURITY-L{self._security_level}] {result} [SECURED]"
    
    def get_cost(self) -> float:
        return super().get_cost() + (50.0 * self._security_level)

class CachingWrapper(Enhancement):
    _cache: Dict[str, str] = {}
    
    def __init__(self, component: Component, ttl: int = 300):
        super().__init__(component)
        self._ttl = ttl
        self._cache_key = f"{id(component)}_{hash(str(component))}"
        self.add_metadata("caching_enabled", True)
        self.add_metadata("cache_ttl", ttl)
    
    def execute(self) -> str:
        if self._cache_key in self._cache:
            cached_result = self._cache[self._cache_key]
            return f"[CACHED] {cached_result}"
        
        result = super().execute()
        self._cache[self._cache_key] = result
        return f"[CACHE-MISS] {result}"
    
    def get_cost(self) -> float:
        return super().get_cost() + 25.0
    
    def clear_cache(self) -> None:
        self._cache.clear()

class LoggingWrapper(Enhancement):
    def __init__(self, component: Component, log_level: str = "INFO"):
        super().__init__(component)
        self._log_level = log_level
        self.add_metadata("logging_enabled", True)
        self.add_metadata("log_level", log_level)
    
    def execute(self) -> str:
        result = super().execute()
        return f"[{self._log_level}] {result} | Cost: ${self.get_cost():.2f}"
    
    def get_cost(self) -> float:
        return super().get_cost() + 10.0

def chain_enhancements(*wrappers):
    def wrapper_func(component: Component) -> Component:
        result = component
        for wrapper_class in wrappers:
            if isinstance(wrapper_class, tuple):
                wrapper_cls, kwargs = wrapper_class
                result = wrapper_cls(result, **kwargs)
            else:
                result = wrapper_class(result)
        return result
    return wrapper_func

if __name__ == "__main__":
    base = BaseService("DataProcessor", 100.0)
    print(f"Base: {base.execute()} - ${base.get_cost()}")
    
    secured = SecurityWrapper(base, security_level=2)
    print(f"Secured: {secured.execute()} - ${secured.get_cost()}")
    
    full_stack = LoggingWrapper(
        CachingWrapper(
            SecurityWrapper(base, security_level=3),
            ttl=600
        ),
        log_level="DEBUG"
    )
    
    print(f"Full Stack 1st: {full_stack.execute()}")
    print(f"Full Stack 2nd: {full_stack.execute()}")
    
    enhanced = chain_enhancements(
        (SecurityWrapper, {"security_level": 1}),
        CachingWrapper,
        (LoggingWrapper, {"log_level": "WARN"})
    )(BaseService("APIGateway", 75.0))
    
    print(f"Enhanced: {enhanced.execute()}")
    print(f"Security Level: {enhanced.get_metadata('security_level')}")