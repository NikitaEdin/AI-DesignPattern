from abc import ABC, abstractmethod

class PaymentProcessor(ABC):
    @abstractmethod
    def pay(self, amount):
        pass

class CreditCardProcessor(PaymentProcessor):
    def __init__(self, card_number):
        self.card_number = card_number[-4:]
    
    def pay(self, amount):
        return f"Paid ${amount} using card ending {self.card_number}"

class PayPalProcessor(PaymentProcessor):
    def __init__(self, email):
        self.email = email
    
    def pay(self, amount):
        return f"Paid ${amount} using PayPal account {self.email}"

class BankTransferProcessor(PaymentProcessor):
    def __init__(self, account):
        self.account = account[-4:]
    
    def pay(self, amount):
        return f"Paid ${amount} using bank account ending {self.account}"

class Checkout:
    def __init__(self):
        self.processor = None
    
    def set_processor(self, processor):
        self.processor = processor
    
    def process_payment(self, amount):
        if not self.processor:
            raise ValueError("No payment method selected")
        return self.processor.pay(amount)

if __name__ == "__main__":
    checkout = Checkout()
    checkout.set_processor(CreditCardProcessor("123456789"))
    print(checkout.process_payment(100))
    checkout.set_processor(PayPalProcessor("user@example.com"))
    print(checkout.process_payment(50))