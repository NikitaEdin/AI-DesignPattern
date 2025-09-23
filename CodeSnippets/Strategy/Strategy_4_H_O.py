from abc import ABC, abstractmethod
from threading import RLock
from typing import Any, Callable, Iterable, List, Optional, Type


class AlgorithmBase(ABC):
    name: str
    input_type: Type
    output_type: Type

    @abstractmethod
    def process(self, data: Any, **kwargs) -> Any:
        pass


class MeanProcessor(AlgorithmBase):
    name = "mean"
    input_type = list
    output_type = float

    def process(self, data: Iterable[float], **kwargs) -> float:
        seq = list(data)
        if len(seq) == 0:
            raise ValueError("empty input for mean")
        return sum(seq) / len(seq)


class SumProcessor(AlgorithmBase):
    name = "sum"
    input_type = list
    output_type = float

    def process(self, data: Iterable[float], **kwargs) -> float:
        seq = list(data)
        return float(sum(seq))


class DefaultZeroProcessor(AlgorithmBase):
    name = "default_zero"
    input_type = list
    output_type = float

    def process(self, data: Iterable[float], **kwargs) -> float:
        return 0.0


class ProcessorManager:
    def __init__(
        self,
        algorithm: AlgorithmBase,
        fallback: Optional[AlgorithmBase] = None,
        validators: Optional[List[Callable[[Any], None]]] = None,
        enable_history: bool = True,
    ):
        if not isinstance(algorithm, AlgorithmBase):
            raise TypeError("algorithm must implement AlgorithmBase")
        if fallback is not None and not isinstance(fallback, AlgorithmBase):
            raise TypeError("fallback must implement AlgorithmBase or be None")
        if fallback is not None:
            # Ensure fallback can accept the same kind of input the primary expects
            if not self._issubclass_safe(algorithm.input_type, fallback.input_type):
                raise ValueError("fallback input_type is incompatible with primary input_type")
        self._lock = RLock()
        self.algorithm = algorithm
        self.fallback = fallback
        self.validators = list(validators) if validators else []
        self._history: Optional[List[dict]] = [] if enable_history else None

    @staticmethod
    def _issubclass_safe(a, b) -> bool:
        try:
            return issubclass(a, b)
        except Exception:
            return False

    def update_algorithm(self, new_algorithm: AlgorithmBase):
        if not isinstance(new_algorithm, AlgorithmBase):
            raise TypeError("new_algorithm must implement AlgorithmBase")
        with self._lock:
            if self.fallback is not None and not self._issubclass_safe(new_algorithm.input_type, self.fallback.input_type):
                raise ValueError("new algorithm's input_type incompatible with existing fallback")
            self.algorithm = new_algorithm

    def execute(self, data: Any, **kwargs) -> Any:
        with self._lock:
            try:
                for v in self.validators:
                    v(data, **kwargs)
                result = self.algorithm.process(data, **kwargs)
                self._record(True, self.algorithm.name, data, result=result)
                return result
            except Exception as exc_primary:
                if self.fallback is not None:
                    try:
                        # run validators again for fallback; if they fail, allow fallback.process attempt
                        for v in self.validators:
                            v(data, **kwargs)
                        result = self.fallback.process(data, **kwargs)
                        self._record(True, self.fallback.name, data, result=result, used_fallback=True, cause=str(exc_primary))
                        return result
                    except Exception as exc_fallback:
                        self._record(False, self.fallback.name, data, error=f"{exc_primary} | {exc_fallback}")
                        raise
                else:
                    self._record(False, self.algorithm.name, data, error=str(exc_primary))
                    raise

    def _summarize(self, data: Any) -> str:
        try:
            if isinstance(data, (list, tuple)):
                head = data[:3]
                return f"{type(data).__name__}(len={len(data)}, head={head})"
            return repr(data)
        except Exception:
            return "<unserializable>"

    def _record(self, success: bool, algo_name: str, data: Any, **extra):
        if self._history is None:
            return
        entry = {
            "algorithm": algo_name,
            "success": success,
            "input": self._summarize(data),
            **extra,
        }
        self._history.append(entry)

    def history(self) -> Optional[List[dict]]:
        if self._history is None:
            return None
        return list(self._history)


# Example usage
if __name__ == "__main__":
    mean = MeanProcessor()
    fallback_zero = DefaultZeroProcessor()
    manager = ProcessorManager(mean, fallback=fallback_zero)

    print("Mean of [1,2,3]:", manager.execute([1, 2, 3]))
    print("Mean of [] uses fallback:", manager.execute([]))

    # Swap algorithm to SumProcessor at runtime (compatible with fallback)
    manager.update_algorithm(SumProcessor())
    print("Sum of [4,5]:", manager.execute([4, 5]))

    # Show history
    for entry in manager.history():
        print(entry)