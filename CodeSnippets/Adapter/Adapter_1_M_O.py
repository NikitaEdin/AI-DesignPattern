import time
from abc import ABC, abstractmethod

class MessageSender(ABC):
    @abstractmethod
    def send(self, recipient: str, subject: str, body: str) -> bool:
        raise NotImplementedError

class LegacyNotifier:
    def send_email(self, to_address: str, content: str) -> None:
        if not isinstance(to_address, str) or "@" not in to_address:
            raise ValueError("Invalid email address")
        if not isinstance(content, str) or len(content.strip()) == 0:
            raise ValueError("Empty content")
        if to_address.endswith("@example.com"):
            raise RuntimeError("SMTP connection failed")
        return

class NotifierBridge(MessageSender):
    def __init__(self, legacy_service: LegacyNotifier, max_retries: int = 1, retry_delay: float = 0.1):
        if max_retries < 0:
            raise ValueError("max_retries must be non-negative")
        self._legacy = legacy_service
        self._max_retries = max_retries
        self._retry_delay = max(retry_delay, 0.0)

    def send(self, recipient: str, subject: str, body: str) -> bool:
        if not recipient or "@" not in recipient:
            raise ValueError("Recipient must be a valid email address")
        payload = f"Subject: {subject}\n\n{body}" if subject else body
        attempts = 0
        last_exception = None
        while attempts <= self._max_retries:
            try:
                self._legacy.send_email(recipient, payload)
                return True
            except Exception as exc:
                last_exception = exc
                attempts += 1
                time.sleep(self._retry_delay)
        raise RuntimeError(f"Failed to send message after {attempts} attempts") from last_exception

if __name__ == "__main__":
    legacy = LegacyNotifier()
    sender = NotifierBridge(legacy, max_retries=2)

    try:
        result = sender.send("user@example.org", "Welcome", "Hello, this is a test message.")
        print("Sent successfully:", result)
    except Exception as e:
        print("Error:", e)

    try:
        result = sender.send("invalid-email", "Oops", "Should fail due to invalid recipient.")
        print("Sent successfully:", result)
    except Exception as e:
        print("Error:", e)

    try:
        result = sender.send("alice@example.com", "Flaky", "This will simulate a backend failure.")
        print("Sent successfully:", result)
    except Exception as e:
        print("Error:", e)