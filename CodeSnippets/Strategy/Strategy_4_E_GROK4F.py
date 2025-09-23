import abc

class PaymentMethod(abc.ABC):
    @abc.abstractmethod
    def process(self, amount):
        pass

class CreditCard(PaymentMethod):
    def process(self, amount):
        return f"Processed {amount} via credit card"

class PayPal(PaymentMethod):
    def process(self, amount):
        return f"Processed {amount} via PayPal"

class PaymentProcessor:
    def __init__(self, method=None):
        self.method = method
    def set_method(self, method):
        self.method = method
    def process_payment(self, amount):
        return self.method.process(amount)

if __name__ == "__main__":
    processor = PaymentProcessor(CreditCard())
    print(processor.process_payment(100))
    processor.set_method(PayPal())
    print(processor.process_payment(100))