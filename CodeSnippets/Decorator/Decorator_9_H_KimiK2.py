from abc import ABC, abstractmethod
import functools
import time

class DataProcessor(ABC):
    @abstractmethod
    def process(self, data):
        pass

class BaseProcessor(DataProcessor):
    def process(self, data):
        return f"Processing: {data}"

class TimingWrapper(DataProcessor):
    def __init__(self, wrapped):
        self._wrapped = wrapped
    
    def process(self, data):
        start = time.perf_counter()
        result = self._wrapped.process(data)
        elapsed = time.perf_counter() - start
        return f"{result} (took {elapsed:.4f}s)"

class CachingWrapper(DataProcessor):
    def __init__(self, wrapped):
        self._wrapped = wrapped
        self._cache = {}
    
    def process(self, data):
        if data in self._cache:
            return f"{self._cache[data]} (cached)"
        result = self._wrapped.process(data)
        self._cache[data] = result
        return result

class ValidationWrapper(DataProcessor):
    def __init__(self, wrapped):
        self._wrapped = wrapped
    
    def process(self, data):
        if not isinstance(data, str) or len(data.strip()) == 0:
            raise ValueError("Invalid input")
        return self._wrapped.process(data)

if __name__ == "__main__":
    processor = BaseProcessor()
    
    timed = TimingWrapper(processor)
    cached = CachingWrapper(timed)
    validated = ValidationWrapper(cached)
    
    test_data = ["hello", "world", "hello", ""]
    
    for item in test_data:
        try:
            print(validated.process(item))
        except ValueError as e:
            print(f"Error: {e}")