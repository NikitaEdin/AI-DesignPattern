import math

class PaymentProcessor:
    def __init__(self, method):
        if not hasattr(method, 'calculate_fee'):
            raise ValueError("Invalid payment method")
        self.method = method

    def execute(self, amount):
        return self.method.calculate_fee(amount)

class CreditCardHandler:
    def calculate_fee(self, amount):
        return amount * 0.03 + 0.5

class BankTransferHandler:
    def calculate_fee(self, amount):
        return 5.0

class CryptoHandler:
    def calculate_fee(self, amount):
        return max(1, amount * 0.015)

if __name__ == "__main__":
    amount = 200
    handlers = [CreditCardHandler(), BankTransferHandler(), CryptoHandler()]
    for handler in handlers:
        processor = PaymentProcessor(handler)
        fee = processor.execute(amount)
        print(f"{handler.__class__.__name__}: Fee = ${fee:.2f}")