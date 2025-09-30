class PaymentMethod:
    def pay(self, amount):
        pass

class CreditCard(PaymentMethod):
    def pay(self, amount):
        print(f"Paying ${amount} with Credit Card")

class PayPal(PaymentMethod):
    def pay(self, amount):
        print(f"Paying ${amount} with PayPal")

class Cart:
    def __init__(self):
        self.method = None
    
    def check_out(self, amount):
        self.method.pay(amount)

cart = Cart()
cart.method = CreditCard()
cart.check_out(100)
cart.method = PayPal()
cart.check_out(200)