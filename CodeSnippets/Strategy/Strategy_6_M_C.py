from abc import ABC, abstractmethod

class PaymentProcessor(ABC):
    @abstractmethod
    def process_payment(self, amount):
        pass

class CreditCardProcessor(PaymentProcessor):
    def process_payment(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be positive")
        return f"Processing ${amount:.2f} via Credit Card"

class PayPalProcessor(PaymentProcessor):
    def process_payment(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be positive")
        return f"Processing ${amount:.2f} via PayPal"

class BankTransferProcessor(PaymentProcessor):
    def process_payment(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be positive")
        if amount > 10000:
            return f"Processing ${amount:.2f} via Bank Transfer (requires verification)"
        return f"Processing ${amount:.2f} via Bank Transfer"

class PaymentGateway:
    def __init__(self, processor: PaymentProcessor):
        self._processor = processor
    
    def set_processor(self, processor: PaymentProcessor):
        self._processor = processor
    
    def execute_payment(self, amount):
        try:
            return self._processor.process_payment(amount)
        except ValueError as e:
            return f"Payment failed: {e}"

if __name__ == "__main__":
    gateway = PaymentGateway(CreditCardProcessor())
    
    print(gateway.execute_payment(100.50))
    
    gateway.set_processor(PayPalProcessor())
    print(gateway.execute_payment(75.25))
    
    gateway.set_processor(BankTransferProcessor())
    print(gateway.execute_payment(15000))
    print(gateway.execute_payment(-50))