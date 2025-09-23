class PaymentProcessor:
    def __init__(self, method):
        self.method = method
    
    def process(self, amount):
        return self.method.pay(amount)

class CreditCard:
    def pay(self, amount):
        return f"Paid ${amount} with credit card"

class PayPal:
    def pay(self, amount):
        return f"Paid ${amount} with PayPal"

class Bitcoin:
    def pay(self, amount):
        return f"Paid ${amount} with Bitcoin"

if __name__ == "__main__":
    processor = PaymentProcessor(CreditCard())
    print(processor.process(100))
    
    processor = PaymentProcessor(PayPal())
    print(processor.process(50))
    
    processor = PaymentProcessor(Bitcoin())
    print(processor.process(25))