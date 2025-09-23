from abc import ABC, abstractmethod

class PaymentMethod(ABC):
    @abstractmethod
    def process(self, amount, details):
        pass

class CreditCardPayment(PaymentMethod):
    def process(self, amount, details):
        if amount <= 0:
            raise ValueError("Amount must be positive")
        if 'card_number' not in details or len(details['card_number']) != 16:
            raise ValueError("Invalid card number")
        return f"Processed {amount} via credit card ending in {details['card_number'][-4:]}"

class BankTransferPayment(PaymentMethod):
    def process(self, amount, details):
        if amount <= 0:
            raise ValueError("Amount must be positive")
        if 'account' not in details or len(details['account']) < 5:
            raise ValueError("Invalid account details")
        return f"Processed {amount} via bank transfer to account {details['account']}"

class PaymentRegistry:
    _methods = {}

    @classmethod
    def register(cls, name, method_class):
        cls._methods[name] = method_class

    @classmethod
    def create(cls, name):
        if name in cls._methods:
            return cls._methods[name]()
        raise ValueError(f"Unknown payment method: {name}")

class PaymentProcessor:
    def __init__(self, method=None):
        self.method = method

    def set_method(self, method):
        if not isinstance(method, PaymentMethod):
            raise TypeError("Must provide a valid payment method")
        self.method = method

    def pay(self, amount, details):
        if not self.method:
            raise ValueError("No payment method selected")
        try:
            return self.method.process(amount, details)
        except ValueError as e:
            return f"Payment failed due to: {str(e)}"

if __name__ == "__main__":
    PaymentRegistry.register("credit", CreditCardPayment)
    PaymentRegistry.register("bank", BankTransferPayment)

    processor = PaymentProcessor()

    processor.set_method(PaymentRegistry.create("credit"))
    result = processor.pay(150.00, {'card_number': '1234567890123456'})
    print(result)

    processor.set_method(PaymentRegistry.create("bank"))
    result = processor.pay(250.00, {'account': 'ACC12345'})
    print(result)

    result = processor.pay(-50.00, {'account': 'ACC12345'})
    print(result)

    try:
        invalid_method = PaymentRegistry.create("paypal")
    except ValueError as e:
        print(f"Error: {e}")