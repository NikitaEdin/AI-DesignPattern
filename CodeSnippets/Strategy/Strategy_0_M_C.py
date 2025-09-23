from abc import ABC, abstractmethod

class PaymentProcessor(ABC):
    @abstractmethod
    def process_payment(self, amount):
        pass
    
    @abstractmethod
    def validate_payment(self, amount):
        pass

class CreditCardProcessor(PaymentProcessor):
    def __init__(self, card_number):
        self.card_number = card_number
    
    def validate_payment(self, amount):
        return amount > 0 and len(self.card_number) == 16
    
    def process_payment(self, amount):
        if not self.validate_payment(amount):
            raise ValueError("Invalid credit card payment")
        return f"Processed ${amount} via Credit Card ending in {self.card_number[-4:]}"

class PayPalProcessor(PaymentProcessor):
    def __init__(self, email):
        self.email = email
    
    def validate_payment(self, amount):
        return amount > 0 and "@" in self.email
    
    def process_payment(self, amount):
        if not self.validate_payment(amount):
            raise ValueError("Invalid PayPal payment")
        return f"Processed ${amount} via PayPal account {self.email}"

class BankTransferProcessor(PaymentProcessor):
    def __init__(self, account_number):
        self.account_number = account_number
    
    def validate_payment(self, amount):
        return amount > 0 and len(self.account_number) >= 8
    
    def process_payment(self, amount):
        if not self.validate_payment(amount):
            raise ValueError("Invalid bank transfer")
        return f"Processed ${amount} via Bank Transfer from account {self.account_number}"

class PaymentHandler:
    def __init__(self, processor):
        self.processor = processor
    
    def set_processor(self, processor):
        self.processor = processor
    
    def handle_payment(self, amount):
        try:
            return self.processor.process_payment(amount)
        except ValueError as e:
            return f"Payment failed: {e}"

if __name__ == "__main__":
    credit_card = CreditCardProcessor("1234567890123456")
    paypal = PayPalProcessor("user@example.com")
    bank_transfer = BankTransferProcessor("12345678")
    
    handler = PaymentHandler(credit_card)
    print(handler.handle_payment(100))
    
    handler.set_processor(paypal)
    print(handler.handle_payment(50))
    
    handler.set_processor(bank_transfer)
    print(handler.handle_payment(200))