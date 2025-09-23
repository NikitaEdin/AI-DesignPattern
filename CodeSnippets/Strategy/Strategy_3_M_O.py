from abc import ABC, abstractmethod
from random import random
from typing import Optional

class TransientError(Exception):
    pass

class ProcessingMethod(ABC):
    @abstractmethod
    def process(self, amount: float) -> str:
        pass

class CreditCardMethod(ProcessingMethod):
    def process(self, amount: float) -> str:
        if amount <= 0:
            raise ValueError("Amount must be positive")
        if random() < 0.25:
            raise TransientError("Network glitch during credit card processing")
        return f"Charged ${amount:.2f} to credit card"

class PayPalMethod(ProcessingMethod):
    def process(self, amount: float) -> str:
        if amount <= 0:
            raise ValueError("Amount must be positive")
        if random() < 0.2:
            raise TransientError("PayPal timeout")
        return f"Processed ${amount:.2f} via PayPal"

class CryptoMethod(ProcessingMethod):
    def process(self, amount: float) -> str:
        if amount <= 0:
            raise ValueError("Amount must be positive")
        if random() < 0.35:
            raise TransientError("Blockchain congestion")
        return f"Sent ${amount:.2f} in cryptocurrency"

class OrderProcessor:
    def __init__(self, method: ProcessingMethod, retries: int = 3):
        self._method = method
        self._retries = max(0, int(retries))

    def set_method(self, method: ProcessingMethod):
        self._method = method

    def process_order(self, amount: float) -> str:
        if amount <= 0:
            raise ValueError("Order amount must be greater than zero")
        last_error: Optional[Exception] = None
        for attempt in range(1, self._retries + 2):
            try:
                return self._method.process(amount)
            except TransientError as e:
                last_error = e
            except Exception:
                raise
        raise RuntimeError(f"All attempts failed: {last_error}")

if __name__ == "__main__":
    processor = OrderProcessor(CreditCardMethod(), retries=2)
    try:
        print(processor.process_order(49.99))
    except Exception as e:
        print("Failed:", e)

    processor.set_method(PayPalMethod())
    try:
        print(processor.process_order(19.95))
    except Exception as e:
        print("Failed:", e)

    processor.set_method(CryptoMethod())
    try:
        print(processor.process_order(0))  # Will raise validation error
    except Exception as e:
        print("Failed:", e)