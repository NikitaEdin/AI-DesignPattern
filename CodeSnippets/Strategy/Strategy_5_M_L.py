class PaymentMethod():
    def __init__(self, payment_strategy):
        self.payment_strategy = payment_strategy
    
    def calculate_total(self, amount):
        return self.payment_strategy.calculate(amount)

class PaypalPaymentStrategy():
    def calculate(self, amount):
        return amount + 2

class CreditCardPaymentStrategy():
    def calculate(self, amount):
        return amount + 5

if __name__ == "__main__":
    payment_method = PaymentMethod(CreditCardPaymentStrategy())
    total = payment_method.calculate_total(10)
    print(f"Total: {total}")