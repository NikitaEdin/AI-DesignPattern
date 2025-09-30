from abc import ABC, abstractmethod


class PaymentProcessor(ABC):
    @abstractmethod
    def pay(self, amount: float) -> str:
        pass


class CardProcessor(PaymentProcessor):
    def pay(self, amount: float) -> str:
        if amount <= 0:
            raise ValueError("Amount must be positive")
        return f"Paid ${amount:.2f} using Card"


class WalletProcessor(PaymentProcessor):
    def pay(self, amount: float) -> str:
        if amount <= 0:
            raise ValueError("Amount must be positive")
        return f"Paid ${amount:.2f} using Wallet"


class CashProcessor(PaymentProcessor):
    def pay(self, amount: float) -> str:
        if amount <= 0:
            raise ValueError("Amount must be positive")
        return f"Paid ${amount:.2f} using Cash"


class Checkout:
    def __init__(self, processor: PaymentProcessor):
        self.processor = processor

    def set_processor(self, processor: PaymentProcessor):
        self.processor = processor

    def complete_payment(self, amount: float) -> str:
        return self.processor.pay(amount)


if __name__ == "__main__":
    checkout = Checkout(CardProcessor())
    print(checkout.complete_payment(99.99))
    checkout.set_processor(WalletProcessor())
    print(checkout.complete_payment(50.00))