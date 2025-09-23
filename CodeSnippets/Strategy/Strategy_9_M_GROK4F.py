from abc import ABC, abstractmethod

class PaymentMethod(ABC):
    @abstractmethod
    def process_payment(self, amount: float) -> bool:
        pass

class CreditCardPayment(PaymentMethod):
    def __init__(self, card_number: str):
        self.card_number = card_number

    def process_payment(self, amount: float) -> bool:
        if not self.card_number or len(self.card_number) < 13:
            raise ValueError("Invalid card number")
        print(f"Processing credit card payment of ${amount} for {self.card_number}")
        return True

class PayPalPayment(PaymentMethod):
    def __init__(self, email: str):
        self.email = email

    def process_payment(self, amount: float) -> bool:
        if not self.email or '@' not in self.email:
            raise ValueError("Invalid PayPal email")
        print(f"Processing PayPal payment of ${amount} to {self.email}")
        return True

class PaymentProcessor:
    def __init__(self, method: PaymentMethod):
        self.method = method

    def set_method(self, method: PaymentMethod):
        self.method = method

    def execute_payment(self, amount: float) -> bool:
        if amount <= 0:
            raise ValueError("Amount must be positive")
        return self.method.process_payment(amount)

if __name__ == "__main__":
    processor = PaymentProcessor(CreditCardPayment("1234567890123"))
    processor.execute_payment(100.50)

    processor.set_method(PayPalPayment("user@example.com"))
    processor.execute_payment(75.25)