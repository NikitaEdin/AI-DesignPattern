from abc import ABC, abstractmethod
from typing import Dict

class PaymentHandler(ABC):
    @abstractmethod
    def process(self, amount: float, details: Dict) -> bool:
        pass

class CreditCardHandler(PaymentHandler):
    def process(self, amount: float, details: Dict) -> bool:
        if amount <= 0:
            raise ValueError("Payment amount must be positive.")
        card_number = details.get("card_number")
        if not isinstance(card_number, str) or len(card_number) != 16 or not card_number.isdigit():
            raise ValueError("Invalid credit card number.")
        print(f"Charging ${amount} to credit card ending in {card_number[-4:]}")
        return True

class PayPalHandler(PaymentHandler):
    def process(self, amount: float, details: Dict) -> bool:
        if amount <= 0:
            raise ValueError("Payment amount must be positive.")
        email = details.get("email")
        if not isinstance(email, str) or "@" not in email:
            raise ValueError("Invalid PayPal email address.")
        print(f"Processing ${amount} via PayPal to {email}")
        return True

class PaymentGateway:
    def __init__(self, handler: PaymentHandler):
        self.handler: PaymentHandler = handler

    def switch_handler(self, handler: PaymentHandler) -> None:
        self.handler = handler

    def make_payment(self, amount: float, details: Dict) -> bool:
        try:
            return self.handler.process(amount, details)
        except ValueError as e:
            print(f"Payment error: {e}")
            return False

if __name__ == "__main__":
    gateway = PaymentGateway(CreditCardHandler())
    success = gateway.make_payment(99.99, {"card_number": "1234567890123456"})
    print(f"Payment successful: {success}\n")
    gateway.switch_handler(PayPalHandler())
    success = gateway.make_payment(150.00, {"email": "user@example.com"})
    print(f"Payment successful: {success}\n")
    success = gateway.make_payment(-50.00, {"email": "user@example.com"})
    print(f"Payment successful: {success}\n")
    success = gateway.make_payment(100.00, {"email": "invalid-email"})
    print(f"Payment successful: {success}")