import random

class PaymentProcessor:
    def __init__(self, method):
        self.method = method
    
    def checkout(self, amount):
        return self.method.pay(amount)

class CreditCard:
    def pay(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be positive")
        return f"Paid ${amount:.2f} using Credit Card"

class PayPal:
    def pay(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be positive")
        return f"Paid ${amount:.2f} using PayPal"

class Crypto:
    def pay(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be positive")
        return f"Paid ${amount:.2f} using Crypto"

if __name__ == "__main__":
    methods = [CreditCard(), PayPal(), Crypto()]
    for _ in range(3):
        processor = PaymentProcessor(random.choice(methods))
        print(processor.checkout(round(random.uniform(10, 100), 2)))