class PaymentStrategy(object):
    def pay(self, amount):
        raise NotImplementedError()

class CreditCardPaymentStrategy(PaymentStrategy):
    def __init__(self, credit_card):
        self.credit_card = credit_card

    def pay(self, amount):
        if self.credit_card.balance < amount:
            raise ValueError("Insufficient funds")
        self.credit_card.withdraw(amount)

class CashPaymentStrategy(PaymentStrategy):
    def __init__(self, cash):
        self.cash = cash

    def pay(self, amount):
        if self.cash < amount:
            raise ValueError("Insufficient funds")
        self.cash -= amount

class Order(object):
    def __init__(self, payment_strategy):
        self.payment_strategy = payment_strategy
        self.amount = 0

    def calculate_cost(self):
        return self.amount

    def pay(self):
        self.payment_strategy.pay(self.calculate_cost())

def main():
    credit_card = CreditCard("John Doe", "4242424242424242", 100)
    order = Order(CreditCardPaymentStrategy(credit_card))
    order.amount = 50
    order.pay()
    print("Balance: ", credit_card.balance)

main()