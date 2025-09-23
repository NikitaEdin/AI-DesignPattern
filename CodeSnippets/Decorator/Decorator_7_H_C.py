from abc import ABC, abstractmethod
import copy
import time
from collections import OrderedDict

class Component(ABC):
    @abstractmethod
    def operation(self):
        pass
    
    @abstractmethod
    def get_cost(self):
        pass
    
    @abstractmethod
    def get_metadata(self):
        pass

class BasicCoffee(Component):
    def operation(self):
        return "Basic Coffee"
    
    def get_cost(self):
        return 2.50
    
    def get_metadata(self):
        return {"ingredients": ["coffee"], "calories": 5}

class BaseWrapper(Component):
    def __init__(self, component):
        self._component = component
    
    def operation(self):
        return self._component.operation()
    
    def get_cost(self):
        return self._component.get_cost()
    
    def get_metadata(self):
        metadata = self._component.get_metadata()
        return {"ingredients": metadata["ingredients"].copy(), "calories": metadata["calories"]}

class MilkEnhancer(BaseWrapper):
    def operation(self):
        return f"{self._component.operation()} with milk"
    
    def get_cost(self):
        return self._component.get_cost() + 0.50
    
    def get_metadata(self):
        metadata = super().get_metadata()
        metadata["ingredients"].append("milk")
        metadata["calories"] += 30
        return metadata

class SugarEnhancer(BaseWrapper):
    def operation(self):
        return f"{self._component.operation()} with sugar"
    
    def get_cost(self):
        return self._component.get_cost() + 0.25
    
    def get_metadata(self):
        metadata = super().get_metadata()
        metadata["ingredients"].append("sugar")
        metadata["calories"] += 16
        return metadata

class TimingEnhancer(BaseWrapper):
    def __init__(self, component):
        super().__init__(component)
        self.execution_time = 0
    
    def operation(self):
        start_time = time.time()
        result = self._component.operation()
        self.execution_time = time.time() - start_time
        return f"{result} [executed in {self.execution_time:.4f}s]"

class CachingEnhancer(BaseWrapper):
    def __init__(self, component, cache_size=3):
        super().__init__(component)
        self._cache = OrderedDict()
        self._cache_size = cache_size
    
    def operation(self):
        cache_key = hash((type(self._component).__name__, 
                         tuple(sorted(self.get_metadata().get("ingredients", [])))))
        
        if cache_key in self._cache:
            self._cache.move_to_end(cache_key)
            return f"{self._cache[cache_key]} [cached]"
        
        result = self._component.operation()
        
        if len(self._cache) >= self._cache_size:
            self._cache.popitem(last=False)
        
        self._cache[cache_key] = result
        return result

if __name__ == "__main__":
    coffee = BasicCoffee()
    
    enhanced_coffee = CachingEnhancer(
        TimingEnhancer(
            SugarEnhancer(
                MilkEnhancer(coffee)
            )
        )
    )
    
    print(f"Order: {enhanced_coffee.operation()}")
    print(f"Cost: ${enhanced_coffee.get_cost():.2f}")
    print(f"Metadata: {enhanced_coffee.get_metadata()}")
    
    print(f"Cached order: {enhanced_coffee.operation()}")