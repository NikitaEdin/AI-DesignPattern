import threading
from abc import ABC, abstractmethod
from typing import Any, Iterable, List


class OperationBase(ABC):
    supports_empty: bool = True

    @abstractmethod
    def run(self, data: Any) -> Any:
        pass


class SumOperation(OperationBase):
    supports_empty = True

    def run(self, data: Iterable[float]) -> float:
        if data is None:
            raise ValueError("Input is None")
        try:
            total = 0.0
            for x in data:
                total += float(x)
            return total
        except TypeError:
            raise TypeError("Input must be an iterable of numbers")


class ProductOperation(OperationBase):
    supports_empty = False

    def run(self, data: Iterable[float]) -> float:
        if data is None:
            raise ValueError("Input is None")
        iterator = iter(data)
        try:
            first = next(iterator)
        except StopIteration:
            raise ValueError("Empty input not allowed for product")
        prod = float(first)
        for x in iterator:
            prod *= float(x)
        return prod


class SortThenFirstOperation(OperationBase):
    supports_empty = False

    def run(self, data: Iterable[Any]) -> Any:
        if data is None:
            raise ValueError("Input is None")
        try:
            sequence = list(data)
        except TypeError:
            raise TypeError("Input must be iterable")
        if not sequence:
            raise ValueError("Empty input not allowed")
        sequence.sort()
        return sequence[0]


class CompositeOperation(OperationBase):
    def __init__(self, steps: List[OperationBase]):
        if not all(isinstance(s, OperationBase) for s in steps):
            raise TypeError("All steps must inherit OperationBase")
        self.steps = steps
        self.supports_empty = all(s.supports_empty for s in steps)

    def run(self, data: Any) -> Any:
        current = data
        for step in self.steps:
            current = step.run(current)
        return current


class DefaultFallback(OperationBase):
    def __init__(self, value: Any = None):
        self.value = value
        self.supports_empty = True

    def run(self, data: Any) -> Any:
        return self.value


class DataProcessor:
    def __init__(self, operation: OperationBase, fallback: OperationBase = None):
        if not isinstance(operation, OperationBase):
            raise TypeError("operation must inherit OperationBase")
        self._lock = threading.RLock()
        self._operation = operation
        self._fallback = fallback if isinstance(fallback, OperationBase) else DefaultFallback(None)

    def set_operation(self, operation: OperationBase) -> None:
        if not isinstance(operation, OperationBase):
            raise TypeError("operation must inherit OperationBase")
        with self._lock:
            self._operation = operation

    def set_fallback(self, fallback: OperationBase) -> None:
        if not isinstance(fallback, OperationBase):
            raise TypeError("fallback must inherit OperationBase")
        with self._lock:
            self._fallback = fallback

    def _is_empty(self, data: Any) -> bool:
        try:
            return len(data) == 0
        except Exception:
            return False

    def process(self, data: Any) -> Any:
        with self._lock:
            op = self._operation
            fallback = self._fallback
        try:
            if not op.supports_empty and self._is_empty(data):
                raise ValueError("Operation does not accept empty input")
            return op.run(data)
        except Exception:
            try:
                return fallback.run(data)
            except Exception as e:
                raise RuntimeError("Both primary and fallback operations failed") from e


if __name__ == "__main__":
    processor = DataProcessor(SumOperation(), fallback=DefaultFallback(0))
    print(processor.process([1, 2, 3.5]))
    processor.set_operation(ProductOperation())
    print(processor.process([2, 3, 4]))
    try:
        print(processor.process([]))
    except Exception as e:
        print("Error:", e)
    processor.set_fallback(DefaultFallback(1))
    print(processor.process([]))
    composite = CompositeOperation([SortThenFirstOperation(), SumOperation()])
    processor.set_operation(composite)
    print(processor.process([5, 1, 3]))