from abc import ABC, abstractmethod
from threading import RLock
from typing import Iterable, Callable, Optional, Sequence


class Operation(ABC):
    @abstractmethod
    def apply(self, data: Iterable[float]) -> float:
        pass

    def name(self) -> str:
        return self.__class__.__name__


class SumOperation(Operation):
    def __init__(self, transform: Optional[Callable[[float], float]] = None):
        self.transform = transform or (lambda x: x)

    def apply(self, data: Iterable[float]) -> float:
        it = list(data)
        if not it:
            raise ValueError("no data provided")
        return sum(self.transform(x) for x in it)


class ProductOperation(Operation):
    def __init__(self, skip_zeros: bool = True):
        self.skip_zeros = skip_zeros

    def apply(self, data: Iterable[float]) -> float:
        it = list(data)
        if not it:
            raise ValueError("no data provided")
        result = 1.0
        for x in it:
            if x == 0 and self.skip_zeros:
                continue
            result *= x
        return result


class WeightedMeanOperation(Operation):
    def __init__(self, weights: Sequence[float]):
        if not weights:
            raise ValueError("weights must not be empty")
        self.weights = list(weights)

    def apply(self, data: Iterable[float]) -> float:
        values = list(data)
        if not values:
            raise ValueError("no data provided")
        if len(values) != len(self.weights):
            raise ValueError("length of data and weights must match")
        total_weight = sum(self.weights)
        if total_weight == 0:
            raise ValueError("sum of weights must not be zero")
        return sum(v * w for v, w in zip(values, self.weights)) / total_weight


class DefaultOperation(Operation):
    def __init__(self, default_value: float = 0.0):
        self.default_value = default_value

    def apply(self, data: Iterable[float]) -> float:
        return self.default_value


class Processor:
    def __init__(self, operation: Operation, fallback: Optional[Operation] = None):
        if not isinstance(operation, Operation):
            raise TypeError("operation must implement Operation")
        if fallback is not None and not isinstance(fallback, Operation):
            raise TypeError("fallback must implement Operation or be None")
        self._lock = RLock()
        self._operation = operation
        self._fallback = fallback

    def set_operation(self, operation: Operation) -> None:
        if not isinstance(operation, Operation):
            raise TypeError("operation must implement Operation")
        with self._lock:
            self._operation = operation

    def set_fallback(self, fallback: Optional[Operation]) -> None:
        if fallback is not None and not isinstance(fallback, Operation):
            raise TypeError("fallback must implement Operation or be None")
        with self._lock:
            self._fallback = fallback

    def current(self) -> str:
        with self._lock:
            return self._operation.name()

    def run(self, data: Iterable[float]) -> float:
        with self._lock:
            op = self._operation
            fallback = self._fallback
        try:
            return op.apply(data)
        except Exception:
            if fallback is not None:
                return fallback.apply(data)
            raise


if __name__ == "__main__":
    data = [1.5, 2.0, 3.5]
    runner = Processor(SumOperation())
    print("Using:", runner.current(), "->", runner.run(data))

    runner.set_operation(ProductOperation(skip_zeros=False))
    print("Using:", runner.current(), "->", runner.run([2, 3, 4]))

    runner.set_operation(WeightedMeanOperation(weights=[0.2, 0.3, 0.5]))
    print("Using:", runner.current(), "->", runner.run(data))

    runner.set_fallback(DefaultOperation(default_value=-1.0))
    try:
        runner.set_operation(SumOperation())
        print("Empty input with fallback ->", runner.run([]))
    except Exception as e:
        print("Error:", e)

    try:
        runner.set_operation("not-an-operation")  # will raise TypeError
    except Exception as e:
        print("Invalid set operation:", e)