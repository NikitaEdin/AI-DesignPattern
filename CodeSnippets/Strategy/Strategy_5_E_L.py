class PaymentGateway:
    def __init__(self, payment_strategy):
        self.payment_strategy = payment_strategy
    
    def make_payment(self, amount):
        return self.payment_strategy.pay(amount)
    
    def set_payment_strategy(self, payment_strategy):
        self.payment_strategy = payment_strategy

class CreditCardPaymentStrategy:
    def pay(self, amount):
        return "Paying with credit card"

class CashPaymentStrategy:
    def pay(self, amount):
        return "Paying in cash"
    
if __name__ == '__main__':
    payment_gateway = PaymentGateway(CreditCardPaymentStrategy())
    print(payment_gateway.make_payment(10))
    payment_gateway.set_payment_strategy(CashPaymentStrategy())
    print(payment_gateway.make_payment(10))