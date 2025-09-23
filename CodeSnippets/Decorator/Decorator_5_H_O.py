from abc import ABC, abstractmethod
from typing import Any, Callable, List, Optional
import random
import time


class AbstractService(ABC):
    @abstractmethod
    def execute(self, payload: dict) -> dict:
        pass


class BasicService(AbstractService):
    def __init__(self, name: str = "BasicService"):
        self.name = name

    def execute(self, payload: dict) -> dict:
        if payload.get("fail") and random.random() < payload.get("fail_chance", 1.0):
            raise RuntimeError("simulated failure")
        result = {"processed_by": self.name, "input": payload}
        return result


class BaseWrapper(AbstractService):
    def __init__(self, component: AbstractService):
        if not isinstance(component, AbstractService):
            raise TypeError("component must implement AbstractService")
        self._component = component

    def execute(self, payload: dict) -> dict:
        return self._component.execute(payload)

    def chain_types(self) -> List[str]:
        types = []
        current = self
        while True:
            types.append(type(current).__name__)
            comp = getattr(current, "_component", None)
            if comp is None or not isinstance(comp, AbstractService):
                break
            if comp is current:
                break
            current = comp
        return types

    def unwrap_all(self) -> AbstractService:
        current = self
        while getattr(current, "_component", None) is not None and isinstance(current._component, AbstractService):
            current = current._component
        return current

    def __getattr__(self, name: str) -> Any:
        comp = object.__getattribute__(self, "_component")
        return getattr(comp, name)


class LoggingWrapper(BaseWrapper):
    def __init__(self, component: AbstractService, logger: Optional[Callable[[str], None]] = None):
        super().__init__(component)
        self._logger = logger or (lambda msg: print(f"[LOG] {msg}"))

    def execute(self, payload: dict) -> dict:
        start_time = time.time()
        self._logger(f"Starting execution on {type(self._component).__name__} with payload={payload}")
        try:
            result = self._component.execute(payload)
            elapsed = (time.time() - start_time) * 1000
            self._logger(f"Completed in {elapsed:.2f}ms result_keys={list(result.keys())}")
            return result
        except Exception as exc:
            elapsed = (time.time() - start_time) * 1000
            self._logger(f"Failed in {elapsed:.2f}ms with error={exc}")
            raise


class RetryWrapper(BaseWrapper):
    def __init__(self, component: AbstractService, max_attempts: int = 3, backoff: float = 0.1,
                 retry_predicate: Optional[Callable[[Exception], bool]] = None):
        super().__init__(component)
        if max_attempts < 1:
            raise ValueError("max_attempts must be >= 1")
        self._max_attempts = max_attempts
        self._backoff = float(backoff)
        self._predicate = retry_predicate or (lambda exc: True)

    def execute(self, payload: dict) -> dict:
        attempt = 0
        last_exc = None
        while attempt < self._max_attempts:
            attempt += 1
            try:
                return self._component.execute(payload)
            except Exception as exc:
                last_exc = exc
                if not self._predicate(exc):
                    raise
                if attempt >= self._max_attempts:
                    break
                time.sleep(self._backoff * attempt)
        raise last_exc


if __name__ == "__main__":
    service = BasicService(name="CoreProcessor")
    logged = LoggingWrapper(service)
    resilient = RetryWrapper(logged, max_attempts=5, backoff=0.05, retry_predicate=lambda e: isinstance(e, RuntimeError))

    payload_success = {"value": 42}
    payload_flaky = {"value": 99, "fail": True, "fail_chance": 0.7}

    print("Chain:", resilient.chain_types())
    print("Unwrapped:", type(resilient.unwrap_all()).__name__)

    print("=== Successful run ===")
    out1 = resilient.execute(payload_success)
    print("Output:", out1)

    print("\n=== Flaky run (may retry) ===")
    try:
        out2 = resilient.execute(payload_flaky)
        print("Output:", out2)
    except Exception as e:
        print("Final failure after retries:", e)