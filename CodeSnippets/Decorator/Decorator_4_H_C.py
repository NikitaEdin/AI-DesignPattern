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
    
    @abstractmethod
    def get_metadata(self) -> Dict[str, Any]:
        pass

class BaseComponent(Component):
    def __init__(self, name: str, base_cost: float = 0.0):
        self._name = name
        self._base_cost = base_cost
    
    def operation(self) -> str:
        return self._name
    
    def get_cost(self) -> float:
        return self._base_cost
    
    def get_metadata(self) -> Dict[str, Any]:
        return {"type": "base", "name": self._name, "layers": 0}

class ComponentWrapper(Component):
    def __init__(self, component: Component):
        self._wrapped = component
        self._modifications: List[str] = []
    
    @property
    def wrapped(self) -> Component:
        return self._wrapped
    
    def operation(self) -> str:
        return self._wrapped.operation()
    
    def get_cost(self) -> float:
        return self._wrapped.get_cost()
    
    def get_metadata(self) -> Dict[str, Any]:
        metadata = self._wrapped.get_metadata()
        metadata["layers"] += 1
        metadata["modifications"] = getattr(metadata, "modifications", []) + self._modifications
        return metadata
    
    def __getattr__(self, name: str) -> Any:
        return getattr(self._wrapped, name)

class EnhancementWrapper(ComponentWrapper):
    def __init__(self, component: Component, enhancement: str, cost_multiplier: float = 1.2):
        super().__init__(component)
        self._enhancement = enhancement
        self._cost_multiplier = cost_multiplier
        self._modifications.append(f"enhanced_with_{enhancement}")
    
    def operation(self) -> str:
        return f"{self._enhancement}({self._wrapped.operation()})"
    
    def get_cost(self) -> float:
        return self._wrapped.get_cost() * self._cost_multiplier

class FeatureWrapper(ComponentWrapper):
    def __init__(self, component: Component, feature: str, additional_cost: float = 10.0):
        super().__init__(component)
        self._feature = feature
        self._additional_cost = additional_cost
        self._modifications.append(f"feature_{feature}")
    
    def operation(self) -> str:
        return f"{self._wrapped.operation()} + {self._feature}"
    
    def get_cost(self) -> float:
        return self._wrapped.get_cost() + self._additional_cost

def chain_wrap(base_component: Component, *wrappers) -> Component:
    result = base_component
    for wrapper_class, *args in wrappers:
        result = wrapper_class(result, *args)
    return result

def validate_component(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        result = func(self, *args, **kwargs)
        if hasattr(self, '_wrapped') and self._wrapped is None:
            raise ValueError("Invalid component state")
        return result
    return wrapper

class ValidatedWrapper(ComponentWrapper):
    @validate_component
    def operation(self) -> str:
        return super().operation()
    
    @validate_component
    def get_cost(self) -> float:
        return super().get_cost()

if __name__ == "__main__":
    basic_product = BaseComponent("BasicItem", 50.0)
    print(f"Basic: {basic_product.operation()} - ${basic_product.get_cost()}")
    
    enhanced = EnhancementWrapper(basic_product, "Premium", 1.5)
    print(f"Enhanced: {enhanced.operation()} - ${enhanced.get_cost()}")
    
    featured = FeatureWrapper(enhanced, "FastShipping", 15.0)
    print(f"Featured: {featured.operation()} - ${featured.get_cost()}")
    
    final_product = EnhancementWrapper(featured, "Gift", 1.1)
    print(f"Final: {final_product.operation()} - ${final_product.get_cost()}")
    print(f"Metadata: {final_product.get_metadata()}")
    
    chained = chain_wrap(
        BaseComponent("ChainedItem", 30.0),
        (FeatureWrapper, "Express", 20.0),
        (EnhancementWrapper, "Deluxe", 1.8),
        (FeatureWrapper, "Insurance", 5.0)
    )
    print(f"Chained: {chained.operation()} - ${chained.get_cost()}")
    print(f"Chain Metadata: {chained.get_metadata()}")