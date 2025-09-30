from abc import ABC, abstractmethod

class PaymentMethod(ABC):
    @abstractmethod
    def pay(self, amount):
        pass

class CreditCard(PaymentMethod):
    def pay(self, amount):
        return f"Paid ${amount:.2f} using Credit Card"

class PayPal(PaymentMethod):
    def pay(self, amount):
        return f"Paid ${amount:.2f} using PayPal"

class Bitcoin(PaymentMethod):
    def pay(self, amount):
        return f"Paid ${amount:.2f} using Bitcoin"

class Checkout:
    def __init__(self):
        self._method = None

    def set_method(self, method):
        self._method = method

    def checkout(self, amount):
        if self._method is None:
            raise ValueError("No payment method selected")
        return self._method.pay(amount)

if __name__ == "__main__":
    cart = Checkout()
    cart.set_method(CreditCard())
    print(cart.checkout(29.99))
    cart.set_method(PayPal())
    print(cart.checkout(14.50))
    cart.set_method(Bitcoin())
    print(cart.checkout(5.99))