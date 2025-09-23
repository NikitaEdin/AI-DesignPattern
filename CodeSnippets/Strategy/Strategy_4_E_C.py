class Payment:
    def process(self, amount):
        pass

class CreditCard(Payment):
    def process(self, amount):
        return f"Paid ${amount} with credit card"

class PayPal(Payment):
    def process(self, amount):
        return f"Paid ${amount} with PayPal"

class BankTransfer(Payment):
    def process(self, amount):
        return f"Paid ${amount} with bank transfer"

class Checkout:
    def __init__(self, payment_method):
        self.payment_method = payment_method
    
    def complete_purchase(self, amount):
        return self.payment_method.process(amount)

if __name__ == "__main__":
    checkout = Checkout(CreditCard())
    print(checkout.complete_purchase(100))
    
    checkout = Checkout(PayPal())
    print(checkout.complete_purchase(200))
    
    checkout = Checkout(BankTransfer())
    print(checkout.complete_purchase(300))