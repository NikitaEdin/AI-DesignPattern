import time

class Messenger:
    def send(self, text: str) -> str:
        return f"Sending: {text}"

class TimestampWrapper:
    def __init__(self, base: Messenger):
        self._base = base

    def send(self, text: str) -> str:
        ts = time.strftime("%Y-%m-%d %H:%M:%S")
        return self._base.send(f"[{ts}] {text}")

class EncryptWrapper:
    def __init__(self, base: Messenger):
        self._base = base

    def send(self, text: str) -> str:
        if not text:
            raise ValueError("Text cannot be empty")
        encrypted = ''.join(chr(ord(c) + 1) for c in text)
        return self._base.send(encrypted)

if __name__ == "__main__":
    basic = Messenger()
    stamped = TimestampWrapper(basic)
    secure = EncryptWrapper(stamped)
    print(secure.send("Hello World"))