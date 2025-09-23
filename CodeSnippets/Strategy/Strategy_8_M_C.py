from abc import ABC, abstractmethod

class PaymentProcessor(ABC):
    @abstractmethod
    def process_payment(self, amount):
        pass
    
    @abstractmethod
    def validate_payment_data(self, data):
        pass

class CreditCardProcessor(PaymentProcessor):
    def process_payment(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be positive")
        return f"Processing ${amount:.2f} via Credit Card"
    
    def validate_payment_data(self, data):
        return len(data.get('card_number', '')) == 16

class PayPalProcessor(PaymentProcessor):
    def process_payment(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be positive")
        return f"Processing ${amount:.2f} via PayPal"
    
    def validate_payment_data(self, data):
        return '@' in data.get('email', '')

class BankTransferProcessor(PaymentProcessor):
    def process_payment(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be positive")
        return f"Processing ${amount:.2f} via Bank Transfer"
    
    def validate_payment_data(self, data):
        return len(data.get('account_number', '')) >= 8

class CheckoutSystem:
    def __init__(self, processor: PaymentProcessor):
        self._processor = processor
    
    def set_processor(self, processor: PaymentProcessor):
        self._processor = processor
    
    def complete_purchase(self, amount, payment_data):
        if not self._processor.validate_payment_data(payment_data):
            return "Invalid payment data"
        return self._processor.process_payment(amount)

if __name__ == "__main__":
    checkout = CheckoutSystem(CreditCardProcessor())
    
    result1 = checkout.complete_purchase(99.99, {'card_number': '1234567890123456'})
    print(result1)
    
    checkout.set_processor(PayPalProcessor())
    result2 = checkout.complete_purchase(49.99, {'email': 'user@example.com'})
    print(result2)
    
    checkout.set_processor(BankTransferProcessor())
    result3 = checkout.complete_purchase(199.99, {'account_number': '12345678'})
    print(result3)