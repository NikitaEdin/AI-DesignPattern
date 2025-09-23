from abc import ABC, abstractmethod
import sys
import time
from typing import Any, Optional

class Service(ABC):
    @abstractmethod
    def process(self, data: Any) -> Any:
        pass

class BasicService(Service):
    def process(self, data: Any) -> str:
        if data is None:
            raise ValueError("No data provided")
        return f"processed:{data}"

class ServiceWrapper(Service):
    def __init__(self, inner: Service):
        if not isinstance(inner, Service):
            raise TypeError("inner must implement Service")
        self._inner = inner

    def process(self, data: Any) -> Any:
        return self._inner.process(data)

class LoggingWrapper(ServiceWrapper):
    def process(self, data: Any) -> Any:
        now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print(f"[{now}] INPUT -> {data}", file=sys.stdout)
        result = self._inner.process(data)
        print(f"[{now}] OUTPUT -> {result}", file=sys.stdout)
        return result

class RetryWrapper(ServiceWrapper):
    def __init__(self, inner: Service, attempts: int = 3, delay: float = 0.1):
        super().__init__(inner)
        if attempts < 1:
            raise ValueError("attempts must be >= 1")
        self.attempts = attempts
        self.delay = delay

    def process(self, data: Any) -> Any:
        last_exc: Optional[Exception] = None
        for attempt in range(1, self.attempts + 1):
            try:
                return self._inner.process(data)
            except Exception as e:
                last_exc = e
                print(f"Attempt {attempt} failed: {e}", file=sys.stderr)
                time.sleep(self.delay)
        raise last_exc

if __name__ == "__main__":
    core = BasicService()
    logged = LoggingWrapper(core)
    resilient = RetryWrapper(logged, attempts=2, delay=0.05)
    try:
        print(resilient.process("payload"))
        print(resilient.process(None))
    except Exception as e:
        print(f"Final error: {e}", file=sys.stderr)