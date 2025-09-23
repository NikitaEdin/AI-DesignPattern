from abc import ABC, abstractmethod

class PaymentMethod(ABC):
    @abstractmethod
    def pay(self, amount):
        pass

class CreditCard(PaymentMethod):
    def pay(self, amount):
        return f"Paid ${amount} with credit card"

class PayPal(PaymentMethod):
    def pay(self, amount):
        return f"Paid ${amount} with PayPal"

class BankTransfer(PaymentMethod):
    def pay(self, amount):
        return f"Paid ${amount} with bank transfer"

class ShoppingCart:
    def __init__(self):
        self.payment_method = None
    
    def set_payment_method(self, method):
        self.payment_method = method
    
    def checkout(self, amount):
        return self.payment_method.pay(amount)

if __name__ == "__main__":
    cart = ShoppingCart()
    
    cart.set_payment_method(CreditCard())
    print(cart.checkout(100))
    
    cart.set_payment_method(PayPal())
    print(cart.checkout(50))