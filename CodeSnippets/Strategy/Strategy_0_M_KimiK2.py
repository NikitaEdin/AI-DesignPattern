import random

class PaymentProcessor:
    def __init__(self, method):
        self.method = method
    
    def pay(self, amount):
        return self.method.charge(amount)

class CreditCard:
    def charge(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be positive")
        return f"Charged ${amount} to credit card"

class PayPal:
    def charge(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be positive")
        return f"Paid ${amount} via PayPal"

class Crypto:
    def charge(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be positive")
        return f"Transferred ${amount} in cryptocurrency"

if __name__ == "__main__":
    methods = [CreditCard(), PayPal(), Crypto()]
    for _ in range(3):
        processor = PaymentProcessor(random.choice(methods))
        print(processor.pay(random.randint(10, 100)))