from abc import ABC, abstractmethod
from functools import reduce
from operator import mul
from typing import Any, Callable, Iterable, List, Optional, Tuple, TypeVar
import numbers

T = TypeVar("T")
R = TypeVar("R")


class AlgorithmBase(ABC):
    @abstractmethod
    def apply(self, data: Any) -> Any:
        raise NotImplementedError


class AddOperator(AlgorithmBase):
    def apply(self, data: Any) -> Any:
        if data is None:
            raise ValueError("Input cannot be None")
        if isinstance(data, numbers.Number):
            return data
        if isinstance(data, Iterable):
            total = 0
            for x in data:
                if not isinstance(x, numbers.Number):
                    raise TypeError("All elements must be numbers for AddOperator")
                total += x
            return total
        raise TypeError("Unsupported data type for AddOperator")


class MultiplyOperator(AlgorithmBase):
    def apply(self, data: Any) -> Any:
        if data is None:
            raise ValueError("Input cannot be None")
        if isinstance(data, numbers.Number):
            return data
        if isinstance(data, Iterable):
            iterator = iter(data)
            try:
                first = next(iterator)
            except StopIteration:
                return 1
            if not isinstance(first, numbers.Number):
                raise TypeError("All elements must be numbers for MultiplyOperator")
            product = first
            for x in iterator:
                if not isinstance(x, numbers.Number):
                    raise TypeError("All elements must be numbers for MultiplyOperator")
                product *= x
            return product
        raise TypeError("Unsupported data type for MultiplyOperator")


class ConditionalOperator(AlgorithmBase):
    def __init__(self, predicate: Callable[[Any], bool], true_op: AlgorithmBase, false_op: AlgorithmBase):
        if not callable(predicate):
            raise TypeError("predicate must be callable")
        if not isinstance(true_op, AlgorithmBase) or not isinstance(false_op, AlgorithmBase):
            raise TypeError("Operators must derive from AlgorithmBase")
        self.predicate = predicate
        self.true_op = true_op
        self.false_op = false_op

    def apply(self, data: Any) -> Any:
        chosen = self.true_op if self.predicate(data) else self.false_op
        return chosen.apply(data)


class CompositeOperator(AlgorithmBase):
    def __init__(self, operators: Iterable[AlgorithmBase]):
        ops = list(operators)
        if not ops:
            raise ValueError("At least one operator required")
        for op in ops:
            if not isinstance(op, AlgorithmBase):
                raise TypeError("All elements must derive from AlgorithmBase")
        self.operators: List[AlgorithmBase] = ops

    def apply(self, data: Any) -> Any:
        result = data
        for op in self.operators:
            result = op.apply(result)
        return result


class FallbackOperator(AlgorithmBase):
    def __init__(self, primary: AlgorithmBase, fallback: AlgorithmBase, catch_exceptions: Optional[Tuple[type, ...]] = None):
        if not isinstance(primary, AlgorithmBase) or not isinstance(fallback, AlgorithmBase):
            raise TypeError("Operators must derive from AlgorithmBase")
        self.primary = primary
        self.fallback = fallback
        self.catch_exceptions = catch_exceptions or (Exception,)

    def apply(self, data: Any) -> Any:
        try:
            return self.primary.apply(data)
        except self.catch_exceptions:
            return self.fallback.apply(data)


class Processor:
    def __init__(self, operator: AlgorithmBase):
        self.set_operator(operator)

    def set_operator(self, operator: AlgorithmBase) -> None:
        if not isinstance(operator, AlgorithmBase):
            raise TypeError("operator must derive from AlgorithmBase")
        self._operator = operator

    def process(self, data: Any) -> Any:
        return self._operator.apply(data)

    def __call__(self, data: Any) -> Any:
        return self.process(data)


if __name__ == "__main__":
    data = [1, 2, 3, 4]

    adder = AddOperator()
    multiplier = MultiplyOperator()

    proc = Processor(adder)
    print("Sum:", proc.process(data))

    proc.set_operator(multiplier)
    print("Product:", proc.process(data))

    composite = CompositeOperator([adder, lambda_op := MultiplyOperator()])
    proc.set_operator(composite)
    print("Composite (sum then multiply treated as scalar):", proc.process(data))

    cond = ConditionalOperator(lambda d: (sum(d) if isinstance(d, Iterable) else d) > 10, multiplier, adder)
    proc.set_operator(cond)
    print("Conditional (>10 -> product else sum):", proc.process(data))

    def risky_apply(data):
        if isinstance(data, Iterable) and any(x < 0 for x in data):
            raise ValueError("Negative not allowed")
        return sum(data)

    class RiskyOperator(AlgorithmBase):
        def apply(self, data: Any) -> Any:
            return risky_apply(data)

    fallback = FallbackOperator(RiskyOperator(), adder, catch_exceptions=(ValueError,))
    proc.set_operator(fallback)
    print("Fallback with positive data:", proc.process([1, 2, 3]))
    print("Fallback with negative data (uses adder):", proc.process([1, -5, 3]))