from abc import ABC, abstractmethod

class PaymentProcessor(ABC):
    @abstractmethod
    def process_payment(self, amount):
        pass
    
    @abstractmethod
    def get_fee(self, amount):
        pass

class CreditCardProcessor(PaymentProcessor):
    def process_payment(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be positive")
        return f"Processing ${amount:.2f} via Credit Card"
    
    def get_fee(self, amount):
        return amount * 0.029

class PayPalProcessor(PaymentProcessor):
    def process_payment(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be positive")
        return f"Processing ${amount:.2f} via PayPal"
    
    def get_fee(self, amount):
        return amount * 0.034 + 0.30

class BankTransferProcessor(PaymentProcessor):
    def process_payment(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be positive")
        return f"Processing ${amount:.2f} via Bank Transfer"
    
    def get_fee(self, amount):
        return 2.50 if amount > 100 else 0

class ShoppingCart:
    def __init__(self):
        self.processor = None
        
    def set_payment_method(self, processor):
        self.processor = processor
        
    def checkout(self, amount):
        if not self.processor:
            raise ValueError("No payment method selected")
        
        fee = self.processor.get_fee(amount)
        total = amount + fee
        result = self.processor.process_payment(total)
        return f"{result} (Fee: ${fee:.2f})"

if __name__ == "__main__":
    cart = ShoppingCart()
    
    cart.set_payment_method(CreditCardProcessor())
    print(cart.checkout(100))
    
    cart.set_payment_method(PayPalProcessor())
    print(cart.checkout(100))
    
    cart.set_payment_method(BankTransferProcessor())
    print(cart.checkout(100))