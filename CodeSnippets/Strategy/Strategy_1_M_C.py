from abc import ABC, abstractmethod

class PaymentProcessor(ABC):
    @abstractmethod
    def process_payment(self, amount):
        pass
    
    @abstractmethod
    def validate_payment(self, payment_details):
        pass

class CreditCardProcessor(PaymentProcessor):
    def process_payment(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be positive")
        return f"Processing ${amount:.2f} via Credit Card"
    
    def validate_payment(self, payment_details):
        return len(payment_details.get('card_number', '')) == 16

class PayPalProcessor(PaymentProcessor):
    def process_payment(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be positive")
        return f"Processing ${amount:.2f} via PayPal"
    
    def validate_payment(self, payment_details):
        email = payment_details.get('email', '')
        return '@' in email and '.' in email

class BankTransferProcessor(PaymentProcessor):
    def process_payment(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be positive")
        return f"Processing ${amount:.2f} via Bank Transfer"
    
    def validate_payment(self, payment_details):
        account = payment_details.get('account_number', '')
        return len(account) >= 8

class PaymentContext:
    def __init__(self, processor: PaymentProcessor):
        self._processor = processor
    
    def set_processor(self, processor: PaymentProcessor):
        self._processor = processor
    
    def execute_payment(self, amount, payment_details):
        if not self._processor.validate_payment(payment_details):
            return "Payment validation failed"
        return self._processor.process_payment(amount)

if __name__ == "__main__":
    context = PaymentContext(CreditCardProcessor())
    
    credit_details = {'card_number': '1234567890123456'}
    print(context.execute_payment(100.50, credit_details))
    
    context.set_processor(PayPalProcessor())
    paypal_details = {'email': 'user@example.com'}
    print(context.execute_payment(75.25, paypal_details))
    
    context.set_processor(BankTransferProcessor())
    bank_details = {'account_number': '12345678'}
    print(context.execute_payment(200.00, bank_details))