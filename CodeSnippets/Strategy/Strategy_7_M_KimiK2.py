from abc import ABC, abstractmethod

class PaymentProcessor(ABC):
    @abstractmethod
    def pay(self, amount):
        pass

class CreditCardProcessor(PaymentProcessor):
    def pay(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be positive")
        return f"Paid ${amount:.2f} using Credit Card"

class PayPalProcessor(PaymentProcessor):
    def pay(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be positive")
        return f"Paid ${amount:.2f} using PayPal"

class CheckoutSystem:
    def __init__(self, processor: PaymentProcessor):
        self.processor = processor
    
    def process_payment(self, amount):
        return self.processor.pay(amount)

if __name__ == "__main__":
    processors = [CreditCardProcessor(), PayPalProcessor()]
    for processor in processors:
        checkout = CheckoutSystem(processor)
        print(checkout.process_payment(100.00))