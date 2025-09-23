import abc
import time
from typing import Any, Callable, Dict, Tuple


class OperationBase(abc.ABC):
    @abc.abstractmethod
    def run(self, *args, **kwargs) -> Any:
        pass


class SumOperation(OperationBase):
    def run(self, *args, **kwargs) -> Any:
        if not args:
            raise ValueError("No operands provided")
        total = 0
        for v in args:
            total += v
        return total


class MultiplyOperation(OperationBase):
    def run(self, *args, **kwargs) -> Any:
        if not args:
            raise ValueError("No operands provided")
        prod = 1
        for v in args:
            prod *= v
        return prod


class FlakyOperation(OperationBase):
    def __init__(self, fail_rate: float = 0.5):
        self.fail_rate = max(0.0, min(1.0, fail_rate))

    def run(self, *args, **kwargs) -> Any:
        import random
        if random.random() < self.fail_rate:
            raise RuntimeError("Transient failure")
        return sum(args)


class CachingWrapper(OperationBase):
    def __init__(self, inner: OperationBase, max_items: int = 1024):
        self.inner = inner
        self.max_items = max_items
        self._cache: Dict[Tuple[Any, ...], Any] = {}
        self._order: list = []

    def _make_key(self, args, kwargs):
        try:
            return (tuple(args), tuple(sorted(kwargs.items())))
        except Exception:
            return None

    def run(self, *args, **kwargs) -> Any:
        key = self._make_key(args, kwargs)
        if key is None:
            return self.inner.run(*args, **kwargs)
        if key in self._cache:
            return self._cache[key]
        result = self.inner.run(*args, **kwargs)
        if len(self._order) >= self.max_items:
            oldest = self._order.pop(0)
            self._cache.pop(oldest, None)
        self._cache[key] = result
        self._order.append(key)
        return result


class RetryWrapper(OperationBase):
    def __init__(self, inner: OperationBase, attempts: int = 3, delay: float = 0.1):
        self.inner = inner
        self.attempts = max(1, attempts)
        self.delay = max(0.0, delay)

    def run(self, *args, **kwargs) -> Any:
        last_exc = None
        for attempt in range(1, self.attempts + 1):
            try:
                return self.inner.run(*args, **kwargs)
            except Exception as e:
                last_exc = e
                time.sleep(self.delay)
        raise last_exc


class FallbackHandler(OperationBase):
    def __init__(self, primary: OperationBase, fallback: OperationBase):
        self.primary = primary
        self.fallback = fallback

    def run(self, *args, **kwargs) -> Any:
        try:
            return self.primary.run(*args, **kwargs)
        except Exception:
            return self.fallback.run(*args, **kwargs)


class Executor:
    def __init__(self, operation: OperationBase, validator: Callable[..., None] = None, measure_time: bool = False):
        self._operation = operation
        self.validator = validator
        self.measure_time = measure_time

    def set_operation(self, operation: OperationBase):
        self._operation = operation

    def execute(self, *args, **kwargs) -> Dict[str, Any]:
        if self.validator:
            self.validator(*args, **kwargs)
        start = time.perf_counter() if self.measure_time else None
        result = self._operation.run(*args, **kwargs)
        end = time.perf_counter() if self.measure_time else None
        payload = {"result": result}
        if self.measure_time:
            payload["duration_s"] = end - start
        return payload


def positive_validator(*args, **kwargs):
    for v in args:
        if not isinstance(v, (int, float)):
            raise TypeError("Operands must be numeric")
        if v < 0:
            raise ValueError("Negative values not allowed")


if __name__ == "__main__":
    sum_op = SumOperation()
    prod_op = MultiplyOperation()
    flaky = FlakyOperation(fail_rate=0.7)

    cached_sum = CachingWrapper(sum_op)
    retry_flaky = RetryWrapper(flaky, attempts=5, delay=0.05)
    fallback_op = FallbackHandler(retry_flaky, prod_op)

    executor = Executor(operation=cached_sum, validator=positive_validator, measure_time=True)
    print(executor.execute(1, 2, 3))

    executor.set_operation(fallback_op)
    try:
        print(executor.execute(2, 3))
    except Exception as e:
        print("Execution failed:", e)

    executor.set_operation(CachingWrapper(MultiplyOperation()))
    print(executor.execute(4, 5, 6))
    print(executor.execute(4, 5, 6))