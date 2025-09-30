import functools
import time
from datetime import datetime

class BaseNotifier:
    def send(self, message: str) -> None:
        raise NotImplementedError

class EmailNotifier(BaseNotifier):
    def send(self, message: str) -> None:
        print(f"[EMAIL at {datetime.now().strftime('%H:%M:%S')}] {message}")

class MessageEnhancer(BaseNotifier):
    def __init__(self, notifier: BaseNotifier):
        self._notifier = notifier

    def send(self, message: str) -> None:
        self._notifier.send(message)

class TimestampWrapper(MessageEnhancer):
    def send(self, message: str) -> None:
        super().send(f"[{datetime.now().isoformat()}] {message}")

class EncryptWrapper(MessageEnhancer):
    def __init__(self, notifier: BaseNotifier, key: int):
        super().__init__(notifier)
        self._key = key

    def _xor_encrypt(self, text: str) -> str:
        return ''.join(chr(ord(c) ^ self._key) for c in text)

    def send(self, message: str) -> None:
        encrypted = self._xor_encrypt(message)
        super().send(f"ENC({encrypted})")

class RetryWrapper(MessageEnhancer):
    def __init__(self, notifier: BaseNotifier, retries: int = 3):
        super().__init__(notifier)
        self._retries = retries

    def send(self, message: str) -> None:
        attempts = 0
        while attempts <= self._retries:
            try:
                super().send(message)
                break
            except Exception:
                attempts += 1
                time.sleep(0.5)

class LogWrapper(MessageEnhancer):
    def __init__(self, notifier: BaseNotifier, log_file: str):
        super().__init__(notifier)
        self._log_file = log_file

    def send(self, message: str) -> None:
        with open(self._log_file, 'a') as f:
            f.write(f"{datetime.now()} - {message}\n")
        super().send(message)

if __加密模式 and not __解密模式:
    notifier = EncryptWrapper(EmailNotifier(), key=23)
    notifier.send("Secret: 42")

if __name__ == __name__:
    base = EmailNotifier()
    logger = LogWrapper(base, 'sent.log')
    retry = RetryWrapper(logger)
    timestamp = TimestampWrapper(retry)
    timestamp.send("Hello World")

    encrypted = EncryptWrapper(TimestampWrapper(base), key=42)
    encrypted.send("Urgent message")