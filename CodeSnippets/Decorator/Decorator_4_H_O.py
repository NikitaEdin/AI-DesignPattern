from abc import ABC, abstractmethod
import base64
import datetime
import threading
import time

class MessageSender(ABC):
    @abstractmethod
    def send(self, message: str) -> str:
        pass

class BasicSender(MessageSender):
    def __init__(self):
        self.history = []
    def send(self, message: str) -> str:
        if message is None:
            raise ValueError("message is None")
        if not isinstance(message, str):
            raise TypeError("message must be a string")
        if message == "":
            raise ValueError("empty message")
        if len(message) > 10000:
            raise ValueError("message too large")
        self.history.append(message)
        return f"SENT:{message}"

class SenderWrapper(MessageSender):
    def __init__(self, inner: MessageSender):
        if not isinstance(inner, MessageSender):
            raise TypeError("inner must implement MessageSender")
        self._inner = inner
        self._lock = threading.RLock()
    def send(self, message: str) -> str:
        with self._lock:
            msg = self.transform_before(message)
            result = self._inner.send(msg)
            return self.transform_after(result)
    def transform_before(self, message: str) -> str:
        return message
    def transform_after(self, sent_result: str) -> str:
        return sent_result
    def layers(self):
        layers = [self.__class__.__name__]
        inner = self._inner
        while isinstance(inner, SenderWrapper):
            layers.append(inner.__class__.__name__)
            inner = inner._inner
        layers.append(inner.__class__.__name__)
        return layers
    def unwrap(self):
        inner = self._inner
        while isinstance(inner, SenderWrapper):
            inner = inner._inner
        return inner
    def __getattr__(self, name):
        return getattr(self._inner, name)

class TimePrefix(SenderWrapper):
    def transform_before(self, message: str) -> str:
        ts = datetime.datetime.utcnow().isoformat()
        return f"{ts} {message}"

class Base64Layer(SenderWrapper):
    def transform_before(self, message: str) -> str:
        if isinstance(message, str):
            return base64.b64encode(message.encode('utf-8')).decode('ascii')
        return message
    def transform_after(self, sent_result: str) -> str:
        try:
            prefix, payload = sent_result.split(":", 1)
            decoded = base64.b64decode(payload.encode('ascii')).decode('utf-8')
            return f"{prefix}:{decoded}"
        except Exception:
            return sent_result

class RetryLayer(SenderWrapper):
    def __init__(self, inner: MessageSender, attempts: int = 3, delay: float = 0.05):
        super().__init__(inner)
        self.attempts = max(1, int(attempts))
        self.delay = max(0.0, float(delay))
    def send(self, message: str) -> str:
        last_exc = None
        for i in range(self.attempts):
            try:
                return super().send(message)
            except Exception as e:
                last_exc = e
                time.sleep(self.delay * (1 + i))
        raise last_exc

if __name__ == "__main__":
    base = BasicSender()
    layered = TimePrefix(Base64Layer(RetryLayer(base, attempts=2, delay=0.01)))
    print("Layers:", layered.layers())
    try:
        result = layered.send("Hello, 世界")
        print("Result:", result)
    except Exception as e:
        print("Send failed:", type(e).__name__, e)
    try:
        layered.send("")  # should trigger validation and retries
    except Exception as e:
        print("Expected failure on empty message:", type(e).__name__, e)
    print("Underlying history entries:", len(base.history))
    print("First history item (raw stored):", base.history[0] if base.history else None)
    unwrapped = layered.unwrap()
    print("Unwrapped type:", type(unwrapped).__name__)