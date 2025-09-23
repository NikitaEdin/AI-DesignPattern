from abc import ABC, abstractmethod
from functools import wraps
from typing import Dict, Any, Callable
import time

def performance_monitor(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"Algorithm executed in {end - start:.4f} seconds")
        return result
    return wrapper

class SortingAlgorithm(ABC):
    @abstractmethod
    def sort(self, data: list) -> list:
        pass
    
    @property
    @abstractmethod
    def name(self) -> str:
        pass

class BubbleSort(SortingAlgorithm):
    @performance_monitor
    def sort(self, data: list) -> list:
        arr = data.copy()
        n = len(arr)
        for i in range(n):
            swapped = False
            for j in range(0, n - i - 1):
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
                    swapped = True
            if not swapped:
                break
        return arr
    
    @property
    def name(self) -> str:
        return "Bubble Sort"

class QuickSort(SortingAlgorithm):
    @performance_monitor
    def sort(self, data: list) -> list:
        if len(data) <= 1:
            return data
        pivot = data[len(data) // 2]
        left = [x for x in data if x < pivot]
        middle = [x for x in data if x == pivot]
        right = [x for x in data if x > pivot]
        return self.sort(left) + middle + self.sort(right)
    
    @property
    def name(self) -> str:
        return "Quick Sort"

class MergeSort(SortingAlgorithm):
    @performance_monitor
    def sort(self, data: list) -> list:
        if len(data) <= 1:
            return data
        mid = len(data) // 2
        left = self.sort(data[:mid])
        right = self.sort(data[mid:])
        return self._merge(left, right)
    
    def _merge(self, left: list, right: list) -> list:
        result = []
        i = j = 0
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        result.extend(left[i:])
        result.extend(right[j:])
        return result
    
    @property
    def name(self) -> str:
        return "Merge Sort"

class DataProcessor:
    def __init__(self, algorithm: SortingAlgorithm = None):
        self._algorithm = algorithm
        self._registry: Dict[str, SortingAlgorithm] = {}
        self._default_algorithms()
    
    def _default_algorithms(self):
        self.register_algorithm("bubble", BubbleSort())
        self.register_algorithm("quick", QuickSort())
        self.register_algorithm("merge", MergeSort())
        if not self._algorithm:
            self._algorithm = self._registry["quick"]
    
    def set_algorithm(self, algorithm: SortingAlgorithm):
        self._algorithm = algorithm
    
    def register_algorithm(self, key: str, algorithm: SortingAlgorithm):
        self._registry[key] = algorithm
    
    def use_algorithm(self, key: str):
        if key not in self._registry:
            raise ValueError(f"Algorithm '{key}' not registered")
        self._algorithm = self._registry[key]
    
    def process(self, data: list) -> list:
        if not self._algorithm:
            raise RuntimeError("No algorithm set")
        print(f"Using {self._algorithm.name}")
        return self._algorithm.sort(data)
    
    def available_algorithms(self) -> list:
        return list(self._registry.keys())

if __name__ == "__main__":
    import random
    
    data = [random.randint(1, 1000) for _ in range(100)]
    processor = DataProcessor()
    
    print(f"Original data (first 10): {data[:10]}")
    print(f"Available algorithms: {processor.available_algorithms()}")
    print()
    
    for algo in processor.available_algorithms():
        processor.use_algorithm(algo)
        sorted_data = processor.process(data)
        print(f"Result (first 10): {sorted_data[:10]}")
        print()
    
    processor.set_algorithm(QuickSort())
    final_result = processor.process([64, 34, 25, 12, 22, 11, 90])
    print(f"Final result: {final_result}")