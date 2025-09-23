from abc import ABC, abstractmethod

class PaymentProcessor(ABC):
    @abstractmethod
    def execute_payment(self, amount):
        pass

class CreditCardProcessor(PaymentProcessor):
    def execute_payment(self, amount):
        if amount <= 0:
            raise ValueError("Invalid payment amount")
        return f"Processed {amount} via credit card"

class BankTransferProcessor(PaymentProcessor):
    def execute_payment(self, amount):
        if amount <= 0:
            raise ValueError("Invalid payment amount")
        return f"Processed {amount} via bank transfer"

class OrderProcessor:
    def __init__(self):
        self.payment_method = None

    def set_payment_method(self, method):
        if not isinstance(method, PaymentProcessor):
            raise TypeError("Invalid payment method")
        self.payment_method = method

    def process_order(self, amount):
        if self.payment_method is None:
            raise ValueError("No payment method set")
        return self.payment_method.execute_payment(amount)

if __name__ == "__main__":
    processor = OrderProcessor()
    processor.set_payment_method(CreditCardProcessor())
    print(processor.process_order(100.0))
    processor.set_payment_method(BankTransferProcessor())
    print(processor.process_order(200.0))