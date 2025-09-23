from abc import ABC, abstractmethod
from datetime import datetime

class Notifier(ABC):
    @abstractmethod
    def send(self, message: str) -> str:
        pass

class SimpleNotifier(Notifier):
    def send(self, message: str) -> str:
        if not isinstance(message, str):
            raise TypeError("message must be a string")
        return message

class MessageWrapper(Notifier):
    def __init__(self, component: Notifier):
        if not isinstance(component, Notifier):
            raise TypeError("component must implement Notifier")
        self._component = component
        self.enabled = True

    def send(self, message: str) -> str:
        return self._component.send(message)

class EncryptionLayer(MessageWrapper):
    def __init__(self, component: Notifier, shift: int = 3):
        super().__init__(component)
        if not isinstance(shift, int):
            raise TypeError("shift must be an integer")
        self._shift = shift % 95

    def send(self, message: str) -> str:
        msg = super().send(message)
        if not self.enabled:
            return msg
        try:
            transformed = []
            for ch in msg:
                code = ord(ch)
                if 32 <= code <= 126:
                    transformed.append(chr((code - 32 + self._shift) % 95 + 32))
                else:
                    transformed.append(ch)
            return ''.join(transformed)
        except Exception as e:
            raise RuntimeError("encryption failed") from e

class TimestampLayer(MessageWrapper):
    def send(self, message: str) -> str:
        msg = super().send(message)
        if not self.enabled:
            return msg
        ts = datetime.utcnow().isoformat() + "Z"
        return f"[{ts}] {msg}"

class UppercaseLayer(MessageWrapper):
    def send(self, message: str) -> str:
        msg = super().send(message)
        if not self.enabled:
            return msg
        if not isinstance(msg, str):
            raise TypeError("inner component produced non-string")
        return msg.upper()

if __name__ == "__main__":
    base = SimpleNotifier()
    chain = EncryptionLayer(TimestampLayer(UppercaseLayer(base)), shift=5)
    original = "Hello, World! 123"
    print("Original:", original)
    result = chain.send(original)
    print("Processed:", result)
    chain.enabled = False
    print("Chain disabled:", chain.send(original))
    # Toggle a sub-layer
    chain._component._component.enabled = False  # disable UppercaseLayer
    print("Uppercase disabled:", chain.send(original))