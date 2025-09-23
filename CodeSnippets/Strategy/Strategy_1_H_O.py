from abc import ABC, abstractmethod
from threading import RLock
from typing import Any, Dict, Tuple
import time
import math

class Operation(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def execute(self, data: Any) -> Any:
        pass

class SumOperation(Operation):
    @property
    def name(self) -> str:
        return "sum"

    def execute(self, data: Any) -> float:
        if isinstance(data, (list, tuple)):
            nums = [float(x) for x in data]
            return sum(nums)
        raise TypeError("SumOperation requires a list or tuple of numbers")

class ProductOperation(Operation):
    @property
    def name(self) -> str:
        return "product"

    def execute(self, data: Any) -> float:
        if isinstance(data, (list, tuple)):
            result = 1.0
            for x in data:
                result *= float(x)
            return result
        raise TypeError("ProductOperation requires a list or tuple of numbers")

class DivideOperation(Operation):
    @property
    def name(self) -> str:
        return "divide"

    def execute(self, data: Any) -> float:
        if isinstance(data, (list, tuple)) and len(data) == 2:
            a, b = float(data[0]), float(data[1])
            if b == 0:
                raise ZeroDivisionError("division by zero")
            return a / b
        raise TypeError("DivideOperation requires a tuple/list of two numbers")

class RetryWrapper(Operation):
    def __init__(self, wrapped: Operation, attempts: int = 3, delay: float = 0.1):
        if not isinstance(wrapped, Operation):
            raise TypeError("wrapped must be an Operation")
        self._wrapped = wrapped
        self._attempts = max(1, int(attempts))
        self._delay = max(0.0, float(delay))

    @property
    def name(self) -> str:
        return f"retry({self._wrapped.name})"

    def execute(self, data: Any) -> Any:
        last_exc = None
        for i in range(self._attempts):
            try:
                return self._wrapped.execute(data)
            except Exception as e:
                last_exc = e
                time.sleep(self._delay)
        raise last_exc

class Executor:
    def __init__(self, operation: Operation, fallback: Operation = None):
        if not isinstance(operation, Operation):
            raise TypeError("operation must be an Operation")
        if fallback is not None and not isinstance(fallback, Operation):
            raise TypeError("fallback must be an Operation or None")
        self._lock = RLock()
        self._operation = operation
        self._fallback = fallback
        self._cache: Dict[Tuple[int, str], Any] = {}

    def set_operation(self, operation: Operation) -> None:
        if not isinstance(operation, Operation):
            raise TypeError("operation must be an Operation")
        with self._lock:
            self._operation = operation
            self._cache.clear()

    def set_fallback(self, fallback: Operation) -> None:
        if fallback is not None and not isinstance(fallback, Operation):
            raise TypeError("fallback must be an Operation or None")
        with self._lock:
            self._fallback = fallback

    def execute(self, data: Any, use_cache: bool = True, validate: bool = True) -> Any:
        if validate:
            self._validate_data(data)
        op = self._get_operation()
        key = (id(op), repr(data))
        if use_cache:
            with self._lock:
                if key in self._cache:
                    return self._cache[key]
        try:
            result = op.execute(data)
        except Exception:
            fb = self._get_fallback()
            if fb is not None:
                result = fb.execute(data)
            else:
                raise
        if use_cache:
            with self._lock:
                self._cache[key] = result
        return result

    def _get_operation(self) -> Operation:
        with self._lock:
            return self._operation

    def _get_fallback(self) -> Operation:
        with self._lock:
            return self._fallback

    @staticmethod
    def _validate_data(data: Any) -> None:
        if data is None:
            raise ValueError("data cannot be None")
        if isinstance(data, (list, tuple)):
            if not data:
                raise ValueError("data sequence cannot be empty")
            for x in data:
                if not isinstance(x, (int, float)):
                    raise TypeError("all elements must be numeric")
        elif not isinstance(data, (int, float)):
            raise TypeError("data must be numeric or a sequence of numerics")

if __name__ == "__main__":
    s = SumOperation()
    p = ProductOperation()
    d = DivideOperation()
    executor = Executor(s)
    print("Sum [1,2,3]:", executor.execute([1, 2, 3]))
    print("Sum cached [1,2,3]:", executor.execute([1, 2, 3]))
    executor.set_operation(p)
    print("Product [1,2,3,4]:", executor.execute([1, 2, 3, 4]))
    executor.set_operation(RetryWrapper(d, attempts=2, delay=0.01))
    executor.set_fallback(s)
    print("Divide with fallback (1/0 should fallback to sum):", executor.execute((1, 0)))
    try:
        executor.set_operation("not an operation")
    except TypeError as e:
        print("Caught expected error when setting invalid operation:", e)