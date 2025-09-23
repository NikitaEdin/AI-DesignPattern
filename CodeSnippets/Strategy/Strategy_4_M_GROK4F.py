from abc import ABC, abstractmethod

class PaymentMethod(ABC):
    @abstractmethod
    def process_payment(self, amount: float) -> str:
        pass

class CreditCardPayment(PaymentMethod):
    def process_payment(self, amount: float) -> str:
        if amount <= 0:
            raise ValueError("Amount must be positive")
        return f"Processed {amount} via credit card"

class PayPalPayment(PaymentMethod):
    def process_payment(self, amount: float) -> str:
        if amount <= 0:
            raise ValueError("Amount must be positive")
        return f"Processed {amount} via PayPal"

class Order:
    def __init__(self):
        self._payment_method = None

    def set_payment_method(self, method: PaymentMethod):
        self._payment_method = method

    def pay(self, amount: float) -> str:
        if self._payment_method is None:
            raise ValueError("No payment method set")
        if amount <= 0:
            raise ValueError("Amount must be positive")
        return self._payment_method.process_payment(amount)

if __name__ == "__main__":
    order = Order()
    order.set_payment_method(CreditCardPayment())
    print(order.pay(100.0))
    order.set_payment_method(PayPalPayment())
    print(order.pay(50.0))