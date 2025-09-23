from abc import ABC, abstractmethod
from functools import wraps
from typing import Any, Callable, Dict, List

class Component(ABC):
    @abstractmethod
    def execute(self) -> str:
        pass
    
    @abstractmethod
    def get_cost(self) -> float:
        pass

class BaseService(Component):
    def __init__(self, name: str, cost: float):
        self._name = name
        self._cost = cost
    
    def execute(self) -> str:
        return f"Executing {self._name}"
    
    def get_cost(self) -> float:
        return self._cost

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

class SecurityWrapper(Enhancement):
    def __init__(self, component: Component, auth_level: str = "basic"):
        super().__init__(component)
        self._auth_level = auth_level
        self.add_metadata("security", auth_level)
    
    def execute(self) -> str:
        auth_check = f"[{self._auth_level.upper()} AUTH] "
        return auth_check + self._component.execute()
    
    def get_cost(self) -> float:
        multiplier = {"basic": 1.1, "advanced": 1.3, "enterprise": 1.5}
        return self._component.get_cost() * multiplier.get(self._auth_level, 1.0)

class LoggingWrapper(Enhancement):
    _log_entries: List[str] = []
    
    def __init__(self, component: Component, log_level: str = "INFO"):
        super().__init__(component)
        self._log_level = log_level
        self.add_metadata("logging", log_level)
    
    def execute(self) -> str:
        log_entry = f"[{self._log_level}] Starting execution"
        LoggingWrapper._log_entries.append(log_entry)
        result = self._component.execute()
        LoggingWrapper._log_entries.append(f"[{self._log_level}] Completed execution")
        return result
    
    def get_cost(self) -> float:
        return self._component.get_cost() + 5.0
    
    @classmethod
    def get_logs(cls) -> List[str]:
        return cls._log_entries.copy()

class CachingWrapper(Enhancement):
    _cache: Dict[str, str] = {}
    
    def __init__(self, component: Component, ttl: int = 300):
        super().__init__(component)
        self._ttl = ttl
        self._cache_key = f"{id(component)}_{hash(str(component.__dict__))}"
        self.add_metadata("caching", {"ttl": ttl, "key": self._cache_key})
    
    def execute(self) -> str:
        if self._cache_key in CachingWrapper._cache:
            return f"[CACHED] {CachingWrapper._cache[self._cache_key]}"
        
        result = self._component.execute()
        CachingWrapper._cache[self._cache_key] = result
        return result
    
    def get_cost(self) -> float:
        return self._component.get_cost() * 0.9

def chain_enhancements(component: Component, *wrappers) -> Component:
    result = component
    for wrapper_class, kwargs in wrappers:
        result = wrapper_class(result, **kwargs)
    return result

if __name__ == "__main__":
    base = BaseService("Data Processing", 100.0)
    print(f"Base: {base.execute()} | Cost: ${base.get_cost()}")
    
    secured = SecurityWrapper(base, "enterprise")
    print(f"Secured: {secured.execute()} | Cost: ${secured.get_cost()}")
    
    logged_secured = LoggingWrapper(secured, "DEBUG")
    print(f"Logged+Secured: {logged_secured.execute()} | Cost: ${logged_secured.get_cost()}")
    
    full_service = CachingWrapper(logged_secured, ttl=600)
    print(f"Full Service: {full_service.execute()} | Cost: ${full_service.get_cost()}")
    print(f"Cached Run: {full_service.execute()}")
    
    chained = chain_enhancements(
        BaseService("API Service", 50.0),
        (SecurityWrapper, {"auth_level": "advanced"}),
        (LoggingWrapper, {"log_level": "WARN"}),
        (CachingWrapper, {"ttl": 120})
    )
    print(f"Chained: {chained.execute()} | Cost: ${chained.get_cost()}")
    
    print(f"Metadata: {chained.get_metadata()}")
    print(f"Logs: {LoggingWrapper.get_logs()}")