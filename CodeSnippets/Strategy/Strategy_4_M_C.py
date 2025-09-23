from abc import ABC, abstractmethod

class PaymentProcessor(ABC):
    @abstractmethod
    def process_payment(self, amount):
        pass

class CreditCardProcessor(PaymentProcessor):
    def __init__(self, card_number):
        self.card_number = card_number[-4:]
    
    def process_payment(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be positive")
        return f"Charged ${amount:.2f} to credit card ending in {self.card_number}"

class PayPalProcessor(PaymentProcessor):
    def __init__(self, email):
        self.email = email
    
    def process_payment(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be positive")
        return f"Charged ${amount:.2f} via PayPal account {self.email}"

class BankTransferProcessor(PaymentProcessor):
    def __init__(self, account_number):
        self.account_number = account_number[-4:]
    
    def process_payment(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be positive")
        return f"Transferred ${amount:.2f} from bank account ending in {self.account_number}"

class ShoppingCart:
    def __init__(self):
        self.payment_method = None
        self.total = 0
    
    def set_payment_method(self, processor):
        self.payment_method = processor
    
    def set_total(self, amount):
        self.total = amount
    
    def checkout(self):
        if not self.payment_method:
            raise ValueError("No payment method selected")
        return self.payment_method.process_payment(self.total)

if __name__ == "__main__":
    cart = ShoppingCart()
    cart.set_total(99.99)
    
    credit_card = CreditCardProcessor("1234567890123456")
    cart.set_payment_method(credit_card)
    print(cart.checkout())
    
    paypal = PayPalProcessor("user@example.com")
    cart.set_payment_method(paypal)
    print(cart.checkout())
    
    bank_transfer = BankTransferProcessor("9876543210")
    cart.set_payment_method(bank_transfer)
    print(cart.checkout())