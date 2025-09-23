from abc import ABC, abstractmethod
from typing import Any, Dict, List
import functools

class Component(ABC):
    @abstractmethod
    def operation(self) -> str:
        pass
    
    @abstractmethod
    def get_cost(self) -> float:
        pass

class BaseWrapper(Component):
    def __init__(self, component: Component):
        self._component = component
        self._metadata: Dict[str, Any] = {}
    
    def operation(self) -> str:
        return self._component.operation()
    
    def get_cost(self) -> float:
        return self._component.get_cost()
    
    def add_metadata(self, key: str, value: Any) -> None:
        self._metadata[key] = value
    
    def get_metadata(self) -> Dict[str, Any]:
        base_meta = getattr(self._component, '_metadata', {})
        return {**base_meta, **self._metadata}

class Coffee(Component):
    def operation(self) -> str:
        return "Simple Coffee"
    
    def get_cost(self) -> float:
        return 2.0

class MilkEnhancer(BaseWrapper):
    def operation(self) -> str:
        return f"{self._component.operation()} + Milk"
    
    def get_cost(self) -> float:
        return self._component.get_cost() + 0.5

class SugarEnhancer(BaseWrapper):
    def operation(self) -> str:
        return f"{self._component.operation()} + Sugar"
    
    def get_cost(self) -> float:
        return self._component.get_cost() + 0.3

class PremiumEnhancer(BaseWrapper):
    def __init__(self, component: Component, multiplier: float = 1.2):
        super().__init__(component)
        self._multiplier = multiplier
        self.add_metadata("premium", True)
    
    def operation(self) -> str:
        return f"Premium [{self._component.operation()}]"
    
    def get_cost(self) -> float:
        return self._component.get_cost() * self._multiplier

class ChainBuilder:
    def __init__(self, base: Component):
        self._component = base
        self._history: List[str] = [type(base).__name__]
    
    def add_enhancement(self, enhancer_class: type, *args, **kwargs):
        self._component = enhancer_class(self._component, *args, **kwargs)
        self._history.append(enhancer_class.__name__)
        return self
    
    def build(self) -> Component:
        self._component.add_metadata("build_history", self._history.copy())
        return self._component

def cached_operation(func):
    @functools.wraps(func)
    def wrapper(self):
        if not hasattr(self, '_cache'):
            self._cache = func(self)
        return self._cache
    return wrapper

class CachedWrapper(BaseWrapper):
    @cached_operation
    def operation(self) -> str:
        self.add_metadata("cached", True)
        return f"Cached: {self._component.operation()}"

if __name__ == "__main__":
    basic_coffee = Coffee()
    print(f"{basic_coffee.operation()} - ${basic_coffee.get_cost():.2f}")
    
    enhanced_coffee = MilkEnhancer(SugarEnhancer(basic_coffee))
    print(f"{enhanced_coffee.operation()} - ${enhanced_coffee.get_cost():.2f}")
    
    premium_coffee = ChainBuilder(Coffee()) \
        .add_enhancement(MilkEnhancer) \
        .add_enhancement(PremiumEnhancer, 1.5) \
        .add_enhancement(CachedWrapper) \
        .build()
    
    print(f"{premium_coffee.operation()} - ${premium_coffee.get_cost():.2f}")
    print(f"Metadata: {premium_coffee.get_metadata()}")
    
    print(f"Second call: {premium_coffee.operation()}")