import abc
import random
import time
from datetime import datetime

class MessageSender(abc.ABC):
    @abc.abstractmethod
    def send(self, message: str) -> None:
        pass

class BasicSender(MessageSender):
    def send(self, message: str) -> None:
        if not isinstance(message, str):
            raise TypeError("message must be a string")
        if random.random() < 0.25:
            raise RuntimeError("transient send failure")
        print(f"Sent: {message}")

class WrapperBase(MessageSender):
    def __init__(self, wrapped: MessageSender):
        if not hasattr(wrapped, "send") or not callable(wrapped.send):
            raise TypeError("wrapped object must implement send(message)")
        self._wrapped = wrapped

    def send(self, message: str) -> None:
        self._wrapped.send(message)

class EncryptionWrapper(WrapperBase):
    def __init__(self, wrapped: MessageSender, shift: int = 3):
        super().__init__(wrapped)
        if not isinstance(shift, int):
            raise TypeError("shift must be an integer")
        self._shift = shift

    def _shift_char(self, ch: str) -> str:
        if 'a' <= ch <= 'z':
            return chr((ord(ch) - 97 + self._shift) % 26 + 97)
        if 'A' <= ch <= 'Z':
            return chr((ord(ch) - 65 + self._shift) % 26 + 65)
        return ch

    def send(self, message: str) -> None:
        encrypted = ''.join(self._shift_char(c) for c in message)
        self._wrapped.send(encrypted)

class LoggingWrapper(WrapperBase):
    def send(self, message: str) -> None:
        timestamp = datetime.utcnow().isoformat()
        print(f"[{timestamp}] Preparing to send message of length {len(message)}")
        self._wrapped.send(message)

class RetryWrapper(WrapperBase):
    def __init__(self, wrapped: MessageSender, retries: int = 3, delay: float = 0.5):
        super().__init__(wrapped)
        if retries < 0:
            raise ValueError("retries must be non-negative")
        self._retries = retries
        self._delay = float(delay)

    def send(self, message: str) -> None:
        last_exc = None
        for attempt in range(1, self._retries + 2):
            try:
                self._wrapped.send(message)
                return
            except Exception as e:
                last_exc = e
                if attempt <= self._retries:
                    time.sleep(self._delay)
                else:
                    raise

if __name__ == "__main__":
    random.seed(42)
    base = BasicSender()
    layered = RetryWrapper(LoggingWrapper(EncryptionWrapper(base, shift=2)), retries=2, delay=0.1)
    messages = ["Hello, World!", "Testing 123", "Another Message"]
    for msg in messages:
        try:
            layered.send(msg)
        except Exception as e:
            print(f"Failed to send '{msg}': {e}")