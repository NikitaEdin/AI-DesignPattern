from abc import ABC, abstractmethod
import functools
import time

class Stream(ABC):
    @abstractmethod
    def write(self, data: str) -> None: ...

class FileOut(Stream):
    def __init__(self, path: str):
        self._path = path
    def write(self, data: str) -> None:
        with open(self._path, 'a', encoding='utf-8') as f:
            f.write(data)

class Wrapper(Stream):
    def __init__(self, wrapped: Stream):
        self._wrapped = wrapped
    def write(self, data: str) -> None:
        self._wrapped.write(data)

class TimestampWrapper(Wrapper):
    def write(self, data: str) -> None:
        prefixed = f"{int(time.time())} {data}"
        super().write(prefixed)

class EncryptionWrapper(Wrapper):
    def __init__(self, wrapped: Stream, key: int = 3):
        super().__init__(wrapped)
        self._key = key
    def _shift(self, ch: str) -> str:
        if ch.isalpha():
            base = ord('A') if ch.isupper() else ord('a')
            return chr((ord(ch) - base + self._key) % 26 + base)
        return ch
    def write(self, data: str) -> None:
        encrypted = ''.join(self._shift(c) for c in data)
        super().write(encrypted)

class RetryWrapper(Wrapper):
    def __init__(self, wrapped: Stream, attempts: int = 3):
        super().__init__(wrapped)
        self._attempts = max(1, attempts)
    def write(self, data: str) -> None:
        for i in range(self._attempts, 0, -1):
            try:
                super().write(data)
                return
            except OSError as e:
                if i == 1:
                    raise
                time.sleep(0.1 * (self._attempts - i + 1))

if __name__ == "__main__":
    sink = FileOut("demo.log")
    pipeline = RetryWrapper(EncryptionWrapper(TimestampWrapper(sink), key=13), attempts=2)
    pipeline.write("Hello, advanced pattern!\n")