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
        fee = self.get_fee(amount)
        return f"Processed ${amount:.2f} via Credit Card (Fee: ${fee:.2f})"
    
    def get_fee(self, amount):
        return amount * 0.03

class PayPalProcessor(PaymentProcessor):
    def process_payment(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be positive")
        fee = self.get_fee(amount)
        return f"Processed ${amount:.2f} via PayPal (Fee: ${fee:.2f})"
    
    def get_fee(self, amount):
        return amount * 0.025

class BankTransferProcessor(PaymentProcessor):
    def process_payment(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be positive")
        fee = self.get_fee(amount)
        return f"Processed ${amount:.2f} via Bank Transfer (Fee: ${fee:.2f})"
    
    def get_fee(self, amount):
        return 2.50 if amount < 1000 else 0

class PaymentGateway:
    def __init__(self, processor):
        self._processor = processor
    
    def set_processor(self, processor):
        self._processor = processor
    
    def execute_payment(self, amount):
        try:
            return self._processor.process_payment(amount)
        except ValueError as e:
            return f"Payment failed: {e}"

if __name__ == "__main__":
    gateway = PaymentGateway(CreditCardProcessor())
    print(gateway.execute_payment(100))
    
    gateway.set_processor(PayPalProcessor())
    print(gateway.execute_payment(100))
    
    gateway.set_processor(BankTransferProcessor())
    print(gateway.execute_payment(1500))
    print(gateway.execute_payment(-50))