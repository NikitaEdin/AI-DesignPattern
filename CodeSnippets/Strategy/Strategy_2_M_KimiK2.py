from abc import ABC, abstractmethod
from typing import List

class PaymentProcessor(ABC):
    @abstractmethod
    def pay(self, amount: float) -> str:
        pass

class CreditCard(PaymentProcessor):
    def __init__(self, number: str):
        self.number = number

    def pay(self, amount: float) -> str:
        return f"Charged ${amount} to credit card {self.number}"

class PayPal(PaymentProcessor):
    def __init__(self, email: str):
        self.email = email

    def pay(self, amount: float) -> str:
        return f"Paid ${amount} via PayPal account {self.email}"

class BankTransfer(PaymentProcessor):
    def __init__(self, iban: str):
        self.iban = iban

    def pay(self, amount: float) -> str:
        return f"Transferred ${amount} from account {self.iban}"

class Checkout:
    def __init__(self):
        self._processor: PaymentProcessor | None = None

    def set_processor(self, processor: PaymentProcessor) -> None:
        self._processor = processor

    def checkout(self, amount: float) -> str:
        if not self._processor:
            raise RuntimeError("No payment method set")
        return self._processor.pay(amount)

if __name__ == "__main__":
    cart = Checkout()
    cart.set_processor(CreditCard("1234-5678-9012-3456"))
    print(cart.checkout(99.99))
    cart.set_processor(PayPal("alice@example.com"))
    print(cart.checkout(50.00))
    cart.set_processor(BankTransfer("GB82WEST12345698765432"))
    print(cart.checkout(75.50))