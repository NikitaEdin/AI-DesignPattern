from abc import ABC, abstractmethod
import time
import threading
import random
import logging
from functools import wraps

logging.basicConfig(level=logging.INFO)

class Processor(ABC):
    @abstractmethod
    def process(self, data):
        pass

class PlainProcessor(Processor):
    def process(self, data):
        return f"Result: {data}"

class ProcessorWrapper(Processor):
    def __init__(self, wrapped):
        if wrapped is None or not isinstance(wrapped, Processor):
            raise TypeError("wrapped must be a Processor instance")
        self._wrapped = wrapped

    def process(self, data):
        return self._wrapped.process(data)

    def unwrap(self):
        return self._wrapped

    def replace_inner(self, new_inner):
        if new_inner is None or not isinstance(new_inner, Processor):
            raise TypeError("new_inner must be a Processor instance")
        self._wrapped = new_inner

    def __getattr__(self, name):
        return getattr(self._wrapped, name)

    def __repr__(self):
        return f"<{self.__class__.__name__} wrapping {self._wrapped!r}>"

class TimeStampLayer(ProcessorWrapper):
    def __init__(self, wrapped, fmt="%Y-%m-%d %H:%M:%S", suffix=False):
        super().__init__(wrapped)
        self.fmt = fmt
        self.suffix = suffix

    def process(self, data):
        base = self._wrapped.process(data)
        ts = time.strftime(self.fmt, time.localtime())
        return f"{base} {ts}" if self.suffix else f"{ts} {base}"

class RetryLayer(ProcessorWrapper):
    def __init__(self, wrapped, attempts=3, backoff=0.1, allowed_exceptions=(Exception,)):
        super().__init__(wrapped)
        if attempts < 1:
            raise ValueError("attempts must be >= 1")
        self.attempts = attempts
        self.backoff = float(backoff)
        self.allowed_exceptions = allowed_exceptions

    def process(self, data):
        last_exc = None
        for attempt in range(1, self.attempts + 1):
            try:
                return self._wrapped.process(data)
            except self.allowed_exceptions as exc:
                last_exc = exc
                time.sleep(self.backoff * attempt)
        raise last_exc

class CacheLayer(ProcessorWrapper):
    def __init__(self, wrapped, maxsize=128):
        super().__init__(wrapped)
        self.cache = {}
        self.maxsize = maxsize
        self.lock = threading.Lock()
        self.order = []

    def _key(self, data):
        try:
            hash(data)
            return ("hashable", data)
        except Exception:
            return ("repr", repr(data))

    def process(self, data):
        key = self._key(data)
        with self.lock:
            if key in self.cache:
                self.order.remove(key)
                self.order.append(key)
                return self.cache[key]
        result = self._wrapped.process(data)
        with self.lock:
            if key in self.cache:
                return self.cache[key]
            self.cache[key] = result
            self.order.append(key)
            while len(self.order) > self.maxsize:
                old = self.order.pop(0)
                del self.cache[old]
        return result

class FlakyProcessor(Processor):
    def __init__(self, fail_rate=0.5):
        if not (0 <= fail_rate <= 1):
            raise ValueError("fail_rate must be between 0 and 1")
        self.fail_rate = fail_rate
        self.counter = 0

    def process(self, data):
        self.counter += 1
        if random.random() < self.fail_rate:
            raise RuntimeError(f"transient failure #{self.counter}")
        return f"OK({self.counter}): {data}"

if __name__ == "__main__":
    base = FlakyProcessor(fail_rate=0.6)
    cached = CacheLayer(base, maxsize=50)
    retried = RetryLayer(cached, attempts=4, backoff=0.05, allowed_exceptions=(RuntimeError,))
    stamped = TimeStampLayer(retried, suffix=True)

    for i in range(1, 6):
        data = f"payload-{i%3}"
        try:
            out = stamped.process(data)
            print(out)
        except Exception as e:
            print("Final failure:", e)

    # Demonstrate unwrapping and replacing inner component at runtime
    inner = stamped.unwrap().unwrap()  # access CacheLayer
    if isinstance(inner, CacheLayer):
        inner.replace_inner(PlainProcessor())
    print("After replacement:", stamped.process("payload-1"))