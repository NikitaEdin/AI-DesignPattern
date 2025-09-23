from abc import ABC, abstractmethod

class PaymentProcessor(ABC):
    @abstractmethod
    def process_payment(self, amount):
        pass

class CreditCardProcessor(PaymentProcessor):
    def process_payment(self, amount):
        if amount <= 0:
            raise ValueError("Payment amount must be positive")
        return f"Processed {amount} via credit card"

class PayPalProcessor(PaymentProcessor):
    def process_payment(self, amount):
        if amount <= 0:
            raise ValueError("Payment amount must be positive")
        return f"Processed {amount} via PayPal"

class Checkout:
    def __init__(self, processor: PaymentProcessor):
        self.processor = processor

    def set_processor(self, processor: PaymentProcessor):
        self.processor = processor

    def complete_purchase(self, amount):
        try:
            result = self.processor.process_payment(amount)
            return result
        except ValueError as e:
            return f"Error: {e}"

if __name__ == "__main__":
    credit_processor = CreditCardProcessor()
    paypal_processor = PayPalProcessor()

    checkout = Checkout(credit_processor)
    print(checkout.complete_purchase(100.00))

    checkout.set_processor(paypal_processor)
    print(checkout.complete_purchase(50.00))

    print(checkout.complete_purchase(-10.00))