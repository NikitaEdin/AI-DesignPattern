from __future__ import annotations
import abc
import inspect
import threading
from dataclasses import dataclass
from typing import Any, Callable, Optional


class AlgorithmBase(abc.ABC):
    @abc.abstractmethod
    def execute(self, data: Any) -> Any:
        raise NotImplementedError


class CallableAdapter(AlgorithmBase):
    def __init__(self, func: Callable[[Any], Any]) -> None:
        sig = inspect.signature(func)
        params = list(sig.parameters.values())
        if not params or (
            params[0].kind not in (inspect.Parameter.POSITIONAL_ONLY, inspect.Parameter.POSITIONAL_OR_KEYWORD)
            and not any(p.kind == inspect.Parameter.VAR_POSITIONAL for p in params)
        ):
            raise TypeError("Callable must accept at least one positional argument")
        self._func = func

    def execute(self, data: Any) -> Any:
        return self._func(data)


class NullAlgorithm(AlgorithmBase):
    def execute(self, data: Any) -> Any:
        return data


class CompositeAlgorithm(AlgorithmBase):
    def __init__(self, primary: AlgorithmBase, fallback: Optional[AlgorithmBase] = None) -> None:
        if primary is None:
            raise ValueError("primary algorithm cannot be None")
        self.primary = primary
        self.fallback = fallback or NullAlgorithm()

    def execute(self, data: Any) -> Any:
        try:
            result = self.primary.execute(data)
            return result
        except Exception:
            return self.fallback.execute(data)


class MultiplyAlgorithm(AlgorithmBase):
    def __init__(self, factor: float) -> None:
        self.factor = factor

    def execute(self, data: Any) -> Any:
        if not isinstance(data, (int, float)):
            raise TypeError("MultiplyAlgorithm expects numeric input")
        return data * self.factor


class ReverseAlgorithm(AlgorithmBase):
    def execute(self, data: Any) -> Any:
        try:
            return data[::-1]
        except Exception as exc:
            raise TypeError("ReverseAlgorithm expects a sequence") from exc


class FaultyAlgorithm(AlgorithmBase):
    def execute(self, data: Any) -> Any:
        raise RuntimeError("intentional failure")


@dataclass
class Processor:
    _algorithm: AlgorithmBase = NullAlgorithm()
    _lock: threading.Lock = threading.Lock()

    def set_algorithm(self, algorithm: Any) -> None:
        with self._lock:
            if algorithm is None:
                self._algorithm = NullAlgorithm()
                return
            if isinstance(algorithm, AlgorithmBase):
                self._algorithm = algorithm
                return
            if callable(algorithm):
                adapter = CallableAdapter(algorithm)
                self._algorithm = adapter
                return
            raise TypeError("algorithm must be AlgorithmBase, callable, or None")

    def process(self, data: Any) -> Any:
        alg = self._algorithm
        return alg.execute(data)


if __name__ == "__main__":
    p = Processor()

    p.set_algorithm(MultiplyAlgorithm(3))
    print(p.process(7))

    p.set_algorithm(ReverseAlgorithm())
    print(p.process("hello"))

    def square(x):
        return x * x

    p.set_algorithm(square)
    print(p.process(6))

    primary = FaultyAlgorithm()
    fallback = MultiplyAlgorithm(2)
    composite = CompositeAlgorithm(primary, fallback)
    p.set_algorithm(composite)
    print(p.process(5))

    p.set_algorithm(None)
    print(p.process({"a": 1}))