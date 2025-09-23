from abc import ABC, abstractmethod

class PaymentMethod(ABC):
    @abstractmethod
    def process_payment(self, amount):
        pass

class CreditCardPayment(PaymentMethod):
    def process_payment(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be positive")
        return f"Processed {amount} via Credit Card"

class PayPalPayment(PaymentMethod):
    def process_payment(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be positive")
        return f"Processed {amount} via PayPal"

class PaymentProcessor:
    def __init__(self, method: PaymentMethod):
        self.method = method

    def set_method(self, method: PaymentMethod):
        self.method = method

    def pay(self, amount):
        try:
            return self.method.process_payment(amount)
        except ValueError as e:
            return f"Error: {e}"

if __name__ == "__main__":
    processor = PaymentProcessor(CreditCardPayment())
    print(processor.pay(100))
    processor.set_method(PayPalPayment())
    print(processor.pay(50))
    print(processor.pay(-10))