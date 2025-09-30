import time
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from functools import lru_cache

class ProcessingMethod(ABC):
    def __init__(self, name: str):
        self.name = name
        self._execution_count = 0
        self._total_time = 0.0
    
    @abstractmethod
    def execute(self, data: Dict[str, Any]) -> Dict[str, Any]:
        pass
    
    def get_stats(self) -> Dict[str, float]:
        avg_time = self._total_time / self._execution_count if self._execution_count > 0 else 0
        return {"executions": self._execution_count, "avg_time": avg_time}

class QuickMethod(ProcessingMethod):
    def __init__(self):
        super().__init__("Quick")
    
    def execute(self, data: Dict[str, Any]) -> Dict[str, Any]:
        start = time.time()
        self._execution_count += 1
        result = {"processed": data["value"] * 2, "method": self.name}
        self._total_time += time.time() - start
        return result

class AccurateMethod(ProcessingMethod):
    def __init__(self):
        super().__init__("Accurate")
        self._cache: Dict[tuple, Any] = {}
    
    def execute(self, data: Dict[str, Any]) -> Dict[str, Any]:
        start = time.time()
        self._execution_count += 1
        cache_key = tuple(sorted(data.items()))
        
        if cache_key in self._cache:
            result = self._cache[cache_key]
        else:
            result = {"processed": data["value"] ** 2, "method": self.name}
            self._cache[cache_key] = result
        
        self._total_time += time.time() - start
        return result

class AdaptiveMethod(ProcessingMethod):
    def __init__(self):
        super().__init__("Adaptive")
        self._threshold = 100
        self._quick = QuickMethod()
        self._accurate = AccurateMethod()
    
    def execute(self, data: Dict[str, Any]) -> Dict[str, Any]:
        start = time.time()
        self._execution_count += 1
        
        if data["value"] < self._threshold:
            result = self._quick.execute(data)
        else:
            result = self._accurate.execute(data)
        
        self._total_time += time.time() - start
        return result

class PaymentProcessor:
    def __init__(self):
        self._method: Optional[ProcessingMethod] = None
        self._history: list = []
    
    def set_method(self, method: ProcessingMethod):
        self._method = method
    
    def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        if not self._method:
            raise ValueError("No processing method set")
        
        result = self._method.execute(data)
        self._history.append(result)
        return result
    
    def get_history(self) -> list:
        return self._history.copy()

if __name__ == "__main__":
    processor = PaymentProcessor()
    
    processor.set_method(QuickMethod())
    result1 = processor.process({"value": 10})
    
    processor.set_method(AccurateMethod())
    result2 = processor.process({"value": 5})
    
    processor.set_method(AdaptiveMethod())
    result3 = processor.process({"value": 50})
    result4 = processor.process({"value": 150})
    
    print("Results:", result1, result2, result3, result4)
    print("History:", processor.get_history())