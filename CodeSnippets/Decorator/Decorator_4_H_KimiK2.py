from abc import ABC, abstractmethod
import functools
import time

class DataStream(ABC):
    @abstractmethod
    def write(self, data: str) -> str:
        pass

class PlainStream(DataStream):
    def write(self, data: str) -> str:
        return data

class StreamEnhancer(DataStream):
    def __init__(self, wrapped: DataStream):
        self._wrapped = wrapped

class TimestampWrapper(StreamEnhancer):
    def write(self, data: str) -> str:
        return self._wrapped.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} {data}")

class BracketWrapper(StreamEnhancer):
    def __init__(self, wrapped: DataStream, bracket: str = "[]"):
        super().__init__(wrapped)
        self.bracket = bracket

    def write(self, data: str) -> str:
        return self._wrapped.write(f"{self.bracket[0]}{data}{self.bracket[-1]}")

class RetryWrapper(StreamEnhancer):
    def __init__(self, wrapped: DataStream, attempts: int = 3):
        super().__init__(wrapped)
        self.attempts = attempts

    def write(self, data: str) -> str:
        for i in range(self.attempts):
            try:
                return self._wrapped.write(data)
            except Exception as e:
                if i == self.attempts - 1:
                    raise
                time.sleep(0.1)

class FaultyStream(DataStream):
    def __init__(self, fail_until: int = 2):
        self.count = 0
        self.fail_until = fail_until

    def write(self, data: str) -> str:
        self.count += 1
        if self.count <= self.fail_until:
            raise RuntimeError("Simulated failure")
        return data

if __name__ == "__main__":
    base = PlainStream()
    wrapped = TimestampWrapper(BracketWrapper(base, "<>"))
    print(wrapped.write("hello"))

    fragile = RetryWrapper(FaultyStream(2))
    print(fragile.write("recovered"))