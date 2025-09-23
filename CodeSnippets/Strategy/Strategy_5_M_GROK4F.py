from abc import ABC, abstractmethod

class PaymentMethod(ABC):
    @abstractmethod
    def process_payment(self, amount):
        pass

class CreditCardPayment(PaymentMethod):
    def process_payment(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be positive")
        return f"Processed {amount} via credit card"

class PayPalPayment(PaymentMethod):
    def process_payment(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be positive")
        return f"Processed {amount} via PayPal"

class BankTransferPayment(PaymentMethod):
    def process_payment(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be positive")
        return f"Processed {amount} via bank transfer"

class PaymentProcessor:
    def __init__(self, method: PaymentMethod):
        self.method = method

    def set_payment_method(self, method: PaymentMethod):
        self.method = method

    def execute_payment(self, amount: float):
        try:
            return self.method.process_payment(amount)
        except ValueError as e:
            return f"Error: {e}"

if __name__ == "__main__":
    processor = PaymentProcessor(CreditCardPayment())
    print(processor.execute_payment(100.0))
    processor.set_payment_method(PayPalPayment())
    print(processor.execute_payment(50.0))
    processor.set_payment_method(BankTransferPayment())
    print(processor.execute_payment(200.0))
    print(processor.execute_payment(-10.0))