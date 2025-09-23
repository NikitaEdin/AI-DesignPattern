from abc import ABC, abstractmethod
from typing import Optional

class PaymentProcessor(ABC):
    @abstractmethod
    def process(self, amount: float) -> bool:
        pass

class CreditCardPaymentProcessor(PaymentProcessor):
    def __init__(self, card_number: str, expiry: str):
        self.card_number = card_number
        self.expiry = expiry

    def process(self, amount: float) -> bool:
        if amount <= 0:
            raise ValueError("Amount must be positive")
        if not self._validate_card():
            raise ValueError("Invalid card details")
        # Simulate processing with fee
        effective_amount = amount * 1.03
        print(f"Processing credit card payment of ${effective_amount:.2f}")
        return True

    def _validate_card(self) -> bool:
        return len(self.card_number) == 16 and len(self.expiry) == 5

class PayPalPaymentProcessor(PaymentProcessor):
    def __init__(self, email: str):
        self.email = email

    def process(self, amount: float) -> bool:
        if amount <= 0:
            raise ValueError("Amount must be positive")
        if not self._validate_email():
            raise ValueError("Invalid email")
        # Simulate processing without fee
        print(f"Processing PayPal payment of ${amount:.2f} via {self.email}")
        return True

    def _validate_email(self) -> bool:
        return '@' in self.email and '.' in self.email

class OrderProcessor:
    def __init__(self):
        self._processor: Optional[PaymentProcessor] = None

    def set_processor(self, processor: PaymentProcessor) -> None:
        self._processor = processor

    def execute_payment(self, amount: float) -> bool:
        if self._processor is None:
            raise RuntimeError("No payment processor set")
        try:
            return self._processor.process(amount)
        except ValueError as e:
            print(f"Payment failed: {e}")
            return False
        except Exception as e:
            print(f"Unexpected error: {e}")
            return False

    def fallback_process(self, amount: float) -> bool:
        if self._processor and self._processor.process(amount):
            return True
        # Fallback to default processor
        default = CreditCardPaymentProcessor("1234567890123456", "12/25")
        try:
            return default.process(amount * 0.95)  # Discount for fallback
        except Exception:
            return False

if __name__ == "__main__":
    processor = OrderProcessor()

    # Test credit card
    processor.set_processor(CreditCardPaymentProcessor("1234567890123456", "12/25"))
    success = processor.execute_payment(100.0)
    print(f"Credit card success: {success}\n")

    # Test invalid amount
    success = processor.execute_payment(-50.0)
    print(f"Invalid amount success: {success}\n")

    # Test PayPal
    processor.set_processor(PayPalPaymentProcessor("user@example.com"))
    success = processor.execute_payment(75.0)
    print(f"PayPal success: {success}\n")

    # Test fallback
    processor.set_processor(PayPalPaymentProcessor("invalid-email"))
    success = processor.fallback_process(200.0)
    print(f"Fallback success: {success}")