from abc import ABC, abstractmethod
from typing import Iterable, Tuple
from functools import reduce
import operator

class ProcessorInterface(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def apply(self, values: Tuple[float, ...]) -> float:
        pass

class SumProcessor(ProcessorInterface):
    @property
    def name(self) -> str:
        return "sum"

    def apply(self, values: Tuple[float, ...]) -> float:
        return sum(values)

class ProductProcessor(ProcessorInterface):
    @property
    def name(self) -> str:
        return "product"

    def apply(self, values: Tuple[float, ...]) -> float:
        return reduce(operator.mul, values, 1.0)

class MeanProcessor(ProcessorInterface):
    @property
    def name(self) -> str:
        return "mean"

    def apply(self, values: Tuple[float, ...]) -> float:
        if not values:
            raise ValueError("Cannot compute mean of empty sequence")
        return sum(values) / len(values)

class Calculator:
    def __init__(self, processor: ProcessorInterface):
        self._processor = processor
        self._cache = {}

    def set_processor(self, processor: ProcessorInterface):
        self._processor = processor

    def compute(self, data: Iterable[float]) -> float:
        try:
            values = tuple(float(x) for x in data)
        except Exception as exc:
            raise ValueError("Input data must be numeric iterable") from exc
        key = (self._processor.name, values)
        if key in self._cache:
            return self._cache[key]
        result = self._processor.apply(values)
        self._cache[key] = result
        return result

if __name__ == "__main__":
    data = [2, 3, 5]
    calc = Calculator(SumProcessor())
    try:
        print("Sum:", calc.compute(data))
        print("Sum (cached):", calc.compute(data))
        calc.set_processor(ProductProcessor())
        print("Product:", calc.compute(data))
        calc.set_processor(MeanProcessor())
        print("Mean:", calc.compute(data))
        print("Mean with empty:", end=" ")
        print(calc.compute([]))
    except Exception as e:
        print("Error:", e)