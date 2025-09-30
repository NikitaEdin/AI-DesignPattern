class PaymentMethod:
    def pay(self, amount):
        pass

class CreditCard(PaymentMethod):
    def pay(self, amount):
        print(f"Paid ${amount} using Credit Card")

class PayPal(PaymentMethod):
    def pay(self, amount):
        print(f"Paid ${amount} using PayPal")

class BankTransfer(PaymentMethod):
    def pay(self, amount):
        print(f"Paid ${amount} using Bank Transfer")

class Checkout:
    def __init__(self, method):
        self.method = method
    
    def process(self, amount):
        self.method.pay(amount)

if __name__ == "__main__":
    checkout = Checkout(CreditCard())
    checkout.process(100)
    checkout.method = PayPal()
    checkout.process(200)