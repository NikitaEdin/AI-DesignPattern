from abc import ABC, abstractmethod

class PaymentProcessor(ABC):
    @abstractmethod
    def process_payment(self, amount):
        pass

class CreditCardProcessor(PaymentProcessor):
    def __init__(self, card_number):
        self.card_number = card_number
    
    def process_payment(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be positive")
        return f"Processed ${amount:.2f} via Credit Card ending in {self.card_number[-4:]}"

class PayPalProcessor(PaymentProcessor):
    def __init__(self, email):
        self.email = email
    
    def process_payment(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be positive")
        return f"Processed ${amount:.2f} via PayPal account {self.email}"

class BankTransferProcessor(PaymentProcessor):
    def __init__(self, account_number):
        self.account_number = account_number
    
    def process_payment(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be positive")
        return f"Processed ${amount:.2f} via Bank Transfer to account ***{self.account_number[-3:]}"

class PaymentContext:
    def __init__(self):
        self._processor = None
    
    def set_payment_method(self, processor):
        if not isinstance(processor, PaymentProcessor):
            raise TypeError("Processor must be a PaymentProcessor instance")
        self._processor = processor
    
    def execute_payment(self, amount):
        if self._processor is None:
            raise RuntimeError("No payment processor set")
        return self._processor.process_payment(amount)

if __name__ == "__main__":
    context = PaymentContext()
    
    credit_card = CreditCardProcessor("1234567812345678")
    paypal = PayPalProcessor("user@example.com")
    bank_transfer = BankTransferProcessor("9876543210")
    
    context.set_payment_method(credit_card)
    print(context.execute_payment(100.50))
    
    context.set_payment_method(paypal)
    print(context.execute_payment(75.25))
    
    context.set_payment_method(bank_transfer)
    print(context.execute_payment(200.00))