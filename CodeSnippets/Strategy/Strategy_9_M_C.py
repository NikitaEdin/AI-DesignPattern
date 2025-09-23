from abc import ABC, abstractmethod

class PaymentProcessor(ABC):
    @abstractmethod
    def process_payment(self, amount):
        pass
    
    @abstractmethod
    def validate_details(self):
        pass

class CreditCardProcessor(PaymentProcessor):
    def __init__(self, card_number, cvv):
        self.card_number = card_number
        self.cvv = cvv
    
    def validate_details(self):
        return len(self.card_number) == 16 and len(self.cvv) == 3
    
    def process_payment(self, amount):
        if not self.validate_details():
            raise ValueError("Invalid credit card details")
        return f"Processed ${amount} via Credit Card ending in {self.card_number[-4:]}"

class PayPalProcessor(PaymentProcessor):
    def __init__(self, email):
        self.email = email
    
    def validate_details(self):
        return "@" in self.email and "." in self.email
    
    def process_payment(self, amount):
        if not self.validate_details():
            raise ValueError("Invalid PayPal email")
        return f"Processed ${amount} via PayPal account {self.email}"

class BankTransferProcessor(PaymentProcessor):
    def __init__(self, account_number):
        self.account_number = account_number
    
    def validate_details(self):
        return len(self.account_number) >= 8
    
    def process_payment(self, amount):
        if not self.validate_details():
            raise ValueError("Invalid bank account number")
        return f"Processed ${amount} via Bank Transfer to account ***{self.account_number[-3:]}"

class PaymentContext:
    def __init__(self, processor):
        self.processor = processor
    
    def set_processor(self, processor):
        self.processor = processor
    
    def execute_payment(self, amount):
        try:
            return self.processor.process_payment(amount)
        except ValueError as e:
            return f"Payment failed: {e}"

if __name__ == "__main__":
    credit_card = CreditCardProcessor("1234567890123456", "123")
    paypal = PayPalProcessor("user@example.com")
    bank_transfer = BankTransferProcessor("12345678")
    
    payment_system = PaymentContext(credit_card)
    
    print(payment_system.execute_payment(100.00))
    
    payment_system.set_processor(paypal)
    print(payment_system.execute_payment(75.50))
    
    payment_system.set_processor(bank_transfer)
    print(payment_system.execute_payment(200.00))
    
    invalid_card = CreditCardProcessor("123", "1")
    payment_system.set_processor(invalid_card)
    print(payment_system.execute_payment(50.00))