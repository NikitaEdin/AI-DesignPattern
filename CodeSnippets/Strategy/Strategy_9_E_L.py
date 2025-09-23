class PaymentStrategy:
    def calculate_payment(self, order):
        raise NotImplementedError()

class CreditCardPaymentStrategy(PaymentStrategy):
    def calculate_payment(self, order):
        return order.total * 0.95

class CashOnDeliveryPaymentStrategy(PaymentStrategy):
    def calculate_payment(self, order):
        return order.total

class Order:
    def __init__(self, total):
        self.total = total
        self.payment_strategy = None

    def set_payment_strategy(self, payment_strategy):
        self.payment_strategy = payment_strategy

    def get_payment_amount(self):
        return self.payment_strategy.calculate_payment(self)

# Usage example
order = Order(100)
order.set_payment_strategy(CreditCardPaymentStrategy())
print(order.get_payment_amount()) # Output: 95.0

order = Order(100)
order.set_payment_strategy(CashOnDeliveryPaymentStrategy())
print(order.get_payment_amount()) # Output: 100.0