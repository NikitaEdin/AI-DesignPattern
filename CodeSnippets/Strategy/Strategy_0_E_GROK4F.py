from abc import ABC, abstractmethod

class PaymentMethod(ABC):
    @abstractmethod
    def process(self, amount):
        pass

class CreditCardPayment(PaymentMethod):
    def process(self, amount):
        return f"Charged {amount} to credit card"

class PayPalPayment(PaymentMethod):
    def process(self, amount):
        return f"Transferred {amount} via PayPal"

class PaymentProcessor:
    def __init__(self):
        self.method = None

    def set_method(self, method):
        self.method = method

    def execute_payment(self, amount):
        if self.method:
            return self.method.process(amount)
        return "No payment method selected"

if __name__ == "__main__":
    processor = PaymentProcessor()
    processor.set_method(CreditCardPayment())
    print(processor.execute_payment(100))
    processor.set_method(PayPalPayment())
    print(processor.execute_payment(200))