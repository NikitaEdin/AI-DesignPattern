from abc import ABC, abstractmethod
import random

class Notifier(ABC):
    @abstractmethod
    def notify(self, message: str) -> None:
        pass

class EmailNotifier(Notifier):
    def notify(self, message: str) -> None:
        print(f"Sending email: {message}")

class FailingEmailNotifier(Notifier):
    def notify(self, message: str) -> None:
        if random.random() < 0.7:
            print(f"Attempting to send email: {message}")
            raise RuntimeError("Network failure")
        else:
            print(f"Successfully sent email: {message}")

class NotifierWrapper(Notifier):
    def __init__(self, wrapped: Notifier):
        self.wrapped = wrapped

    def notify(self, message: str) -> None:
        self.wrapped.notify(message)

class LoggingNotifierWrapper(NotifierWrapper):
    def notify(self, message: str) -> None:
        print("Starting notification process")
        try:
            super().notify(message)
            print("Notification process completed")
        except Exception as e:
            print(f"Error during notification: {e}")
            raise

class ValidationNotifierWrapper(NotifierWrapper):
    def notify(self, message: str) -> None:
        if not message or not message.strip():
            raise ValueError("Invalid message: cannot be empty or whitespace only")
        cleaned_message = message.strip()
        super().notify(cleaned_message)

class RetryNotifierWrapper(NotifierWrapper):
    def __init__(self, wrapped: Notifier, max_attempts: int = 3):
        super().__init__(wrapped)
        self.max_attempts = max(1, max_attempts)

    def notify(self, message: str) -> None:
        last_exception = None
        for attempt in range(self.max_attempts):
            try:
                super().notify(message)
                return
            except Exception as e:
                last_exception = e
                print(f"Notification attempt {attempt + 1} failed: {e}")
                if attempt < self.max_attempts - 1:
                    continue
        raise RuntimeError(f"All {self.max_attempts} attempts failed") from last_exception

if __name__ == "__main__":
    base = FailingEmailNotifier()
    logged = LoggingNotifierWrapper(base)
    validated = ValidationNotifierWrapper(logged)
    retry = RetryNotifierWrapper(validated, max_attempts=3)

    print("Testing valid message:")
    try:
        retry.notify("Hello, World!")
    except Exception as e:
        print(f"Final error: {e}")

    print("\nTesting empty message:")
    try:
        retry.notify("")
    except ValueError as e:
        print(f"Validation error: {e}")