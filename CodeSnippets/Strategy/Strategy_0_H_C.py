from abc import ABC, abstractmethod
from functools import wraps
from typing import Any, Dict, List, Optional
import logging

def validate_input(func):
    @wraps(func)
    def wrapper(self, data: List[float], *args, **kwargs):
        if not data or not all(isinstance(x, (int, float)) for x in data):
            raise ValueError("Invalid data: must be non-empty list of numbers")
        return func(self, data, *args, **kwargs)
    return wrapper

class AnalysisMethod(ABC):
    def __init__(self, name: str):
        self.name = name
        self._cache = {}
    
    @abstractmethod
    def execute(self, data: List[float]) -> Dict[str, Any]:
        pass
    
    def clear_cache(self):
        self._cache.clear()

class StatisticalAnalysis(AnalysisMethod):
    def __init__(self):
        super().__init__("Statistical")
    
    @validate_input
    def execute(self, data: List[float]) -> Dict[str, Any]:
        cache_key = tuple(data)
        if cache_key in self._cache:
            return self._cache[cache_key]
        
        result = {
            'mean': sum(data) / len(data),
            'median': sorted(data)[len(data) // 2],
            'min': min(data),
            'max': max(data),
            'range': max(data) - min(data)
        }
        self._cache[cache_key] = result
        return result

class TrendAnalysis(AnalysisMethod):
    def __init__(self):
        super().__init__("Trend")
    
    @validate_input
    def execute(self, data: List[float]) -> Dict[str, Any]:
        cache_key = tuple(data)
        if cache_key in self._cache:
            return self._cache[cache_key]
        
        if len(data) < 2:
            slope = 0
        else:
            n = len(data)
            x_vals = list(range(n))
            sum_x = sum(x_vals)
            sum_y = sum(data)
            sum_xy = sum(x * y for x, y in zip(x_vals, data))
            sum_x2 = sum(x * x for x in x_vals)
            slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x * sum_x)
        
        result = {
            'slope': slope,
            'direction': 'increasing' if slope > 0 else 'decreasing' if slope < 0 else 'stable',
            'strength': abs(slope),
            'volatility': sum(abs(data[i] - data[i-1]) for i in range(1, len(data))) / (len(data) - 1) if len(data) > 1 else 0
        }
        self._cache[cache_key] = result
        return result

class DataProcessor:
    def __init__(self, method: Optional[AnalysisMethod] = None):
        self._method = method or StatisticalAnalysis()
        self.history: List[Dict[str, Any]] = []
    
    def set_method(self, method: AnalysisMethod):
        self._method = method
    
    def process(self, data: List[float]) -> Dict[str, Any]:
        try:
            result = self._method.execute(data)
            result['method'] = self._method.name
            self.history.append({
                'method': self._method.name,
                'data_points': len(data),
                'result': result
            })
            return result
        except Exception as e:
            logging.error(f"Processing failed with {self._method.name}: {e}")
            raise
    
    def get_available_methods(self) -> List[AnalysisMethod]:
        return [StatisticalAnalysis(), TrendAnalysis()]
    
    def clear_history(self):
        self.history.clear()
        if hasattr(self._method, 'clear_cache'):
            self._method.clear_cache()

if __name__ == "__main__":
    processor = DataProcessor()
    sample_data = [10.5, 12.3, 9.8, 15.2, 11.7, 13.9, 14.1, 16.5]
    
    stats_result = processor.process(sample_data)
    print(f"Statistical Analysis: {stats_result}")
    
    processor.set_method(TrendAnalysis())
    trend_result = processor.process(sample_data)
    print(f"Trend Analysis: {trend_result}")
    
    cached_result = processor.process(sample_data)
    print(f"Cached Result: {cached_result}")
    
    print(f"Processing History: {len(processor.history)} entries")