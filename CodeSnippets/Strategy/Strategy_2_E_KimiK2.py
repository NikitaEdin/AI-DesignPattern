class PaymentProcessor:
    def __init__(self, method):
        self.method = method

    def pay(self, amount):
        self.method.process(amount)


class Card:
    def process(self, amount):
        print(f"Paid {amount} using card")


class Cash:
    def process(self, amount):
        print(f"Paid {amount} using cash")


if __name__ == "__main":
    payment = PaymentProcessor(Card())
    payment.pay(100)
    payment.method = Cash()
    payment.pay(50)