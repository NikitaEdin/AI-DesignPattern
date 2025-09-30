class PaymentMethod:
    def pay(self, amount): pass

class CreditCard(PaymentMethod):
    def pay(self, amount):
        print(f"Paid ${amount} via credit card")

class PayPal(PaymentMethod):
    def pay(self, amount):
        print(f"Paid ${amount} via PayPal")

class Crypto(PaymentMethod):
    def pay(self, amount):
        print(f"Paid ${amount} via cryptocurrency")

class Checkout:
    def __init__(self, method: PaymentMethod):
        self.method = method
    def process(self, amount):
        self.method.pay(amount)

if __name__ == "__main__":
    checkout = Checkout(CreditCard())
    checkout.process(100)
    checkout.method = PayPal()
    checkout.process(50)