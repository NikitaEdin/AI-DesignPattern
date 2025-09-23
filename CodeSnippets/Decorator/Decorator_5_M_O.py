import time
import random
from abc import ABC, abstractmethod

class ServiceInterface(ABC):
    @abstractmethod
    def process(self, data):
        pass

class SimpleSender(ServiceInterface):
    def __init__(self, name):
        self.name = name

    def process(self, data):
        if not isinstance(data, str) or not data.strip():
            raise ValueError("data must be a non-empty string")
        if random.random() < 0.3:
            raise RuntimeError("transient network error")
        return f"{self.name} sent: {data}"

class LoggingWrapper(ServiceInterface):
    def __init__(self, wrapped, logger=print):
        if not isinstance(wrapped, ServiceInterface):
            raise TypeError("wrapped must implement ServiceInterface")
        self.wrapped = wrapped
        self.logger = logger

    def process(self, data):
        start = time.time()
        self.logger(f"START -> {self.wrapped.__class__.__name__}")
        try:
            result = self.wrapped.process(data)
            elapsed = time.time() - start
            self.logger(f"OK ({elapsed:.3f}s) -> {result}")
            return result
        except Exception as e:
            elapsed = time.time() - start
            self.logger(f"ERROR ({elapsed:.3f}s) -> {e}")
            raise

class RetryWrapper(ServiceInterface):
    def __init__(self, wrapped, attempts=3, delay=0.2):
        if not isinstance(wrapped, ServiceInterface):
            raise TypeError("wrapped must implement ServiceInterface")
        if attempts < 1:
            raise ValueError("attempts must be >= 1")
        self.wrapped = wrapped
        self.attempts = attempts
        self.delay = delay

    def process(self, data):
        last_exc = None
        for attempt in range(1, self.attempts + 1):
            try:
                return self.wrapped.process(data)
            except Exception as e:
                last_exc = e
                if attempt == self.attempts:
                    break
                time.sleep(self.delay)
        raise last_exc

if __name__ == "__main__":
    random.seed(1)
    sender = SimpleSender("WorkerA")
    service = LoggingWrapper(RetryWrapper(sender, attempts=4))
    try:
        print(service.process("payload-123"))
    except Exception as e:
        print("Final failure:", e)
    try:
        print(service.process("   "))
    except Exception as e:
        print("Validation failure:", e)