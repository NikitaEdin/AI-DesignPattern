from abc import ABC, abstractmethod

class PaymentMethod(ABC):
    @abstractmethod
    def process_payment(self, amount: float) -> str:
        pass

class CreditCardPayment(PaymentMethod):
    def process_payment(self, amount: float) -> str:
        return f"Charged {amount} to credit card"

class PayPalPayment(PaymentMethod):
    def process_payment(self, amount: float) -> str:
        return f"Transferred {amount} via PayPal"

class BankTransferPayment(PaymentMethod):
    def process_payment(self, amount: float) -> str:
        return f"Initiated bank transfer for {amount}"

class PaymentProcessor:
    def __init__(self, method: PaymentMethod):
        self.method = method

    def set_method(self, method: PaymentMethod) -> None:
        self.method = method

    def pay(self, amount: float) -> str:
        if amount <= 0:
            raise ValueError("Payment amount must be positive")
        return self.method.process_payment(amount)

if __name__ == "__main__":
    processor = PaymentProcessor(CreditCardPayment())
    print(processor.pay(100.0))
    processor.set_method(PayPalPayment())
    print(processor.pay(200.0))
    processor.set_method(BankTransferPayment())
    print(processor.pay(300.0))