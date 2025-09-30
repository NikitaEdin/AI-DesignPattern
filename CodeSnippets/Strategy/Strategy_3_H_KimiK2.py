import sys

class PaymentMethod:
    def calculate_fee(self, amount):
        raise NotImplementedError()
    
    def pay(self, amount):
        raise NotImplementedError()

class CreditCardProcessor(PaymentMethod):
    def __init__(self, flat_fee=0.5, percentage=0.02):
        self.flat_fee = flat_fee
        self.percentage = percentage
    
    def calculate_fee(self, amount):
        return self.flat_fee + (amount * self.percentage)
    
    def pay(self, amount):
        total = amount + self.calculate_fee(amount)
        print(f"Credit card payment: ${total:.2f}")
        return total

class PayPalProcessor(PaymentMethod):
    def __init__(self, flat_fee=0.3, percentage=0.025):
        self.flat_fee = flat_fee
        self.percentage = percentage
    
    def calculate_fee(self, amount):
        return self.flat_fee + (amount * self.percentage)
    
    def pay(self, amount):
        total = amount + self.calculate_fee(amount)
        print(f"PayPal payment: ${total:.2f}")
        return total

class BitcoinProcessor(PaymentMethod):
    def __init__(self, flat_fee=0.01, percentage=0.001):
        self.flat_fee = flat_fee
        self.percentage = percentage
    
    def calculate_fee(self, amount):
        return self.flat_fee + (amount * self.percentage)
    
    def pay(self, amount):
        total = amount + self.calculate_fee(amount)
        print(f"Bitcoin payment: ${total:.2f}")
        return total

class Checkout:
    def __init__(self):
        self.processor = None
    
    def set_processor(self, processor):
        self.processor = processor
    
    def finalize(self, amount):
        if self.processor is None:
            raise ValueError("No payment method set")
        if not isinstance(amount, (int, float)) or amount <= 0:
            raise ValueError("Invalid amount")
        return self.processor.pay(amount)

if __name__ == "__main__":
    checkout = Checkout()
    checkout.set_processor(CreditCardProcessor())
    checkout.finalize(100)
    
    checkout.set_processor(PayPalProcessor())
    checkout.finalize(100)
    
    checkout.set_processor(BitcoinProcessor())
    checkout.finalize(100)