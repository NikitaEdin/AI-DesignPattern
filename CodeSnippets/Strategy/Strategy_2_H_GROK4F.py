from abc import ABC, abstractmethod
from typing import Optional

class PaymentMethod(ABC):
    @abstractmethod
    def execute_payment(self, amount: float) -> bool:
        pass

class CreditCardPayment(PaymentMethod):
    def execute_payment(self, amount: float) -> bool:
        if amount <= 0:
            raise ValueError("Amount must be positive")
        if amount > 10000:
            raise ValueError("Amount exceeds credit card limit")
        print(f"Charging {amount} to credit card")
        return True

class PayPalPayment(PaymentMethod):
    def execute_payment(self, amount: float) -> bool:
        if amount <= 0:
            raise ValueError("Amount must be positive")
        fee = amount * 0.03
        total = amount + fee
        if total > 5000:
            raise ValueError("Transaction exceeds PayPal limit after fees")
        print(f"Processing {amount} via PayPal with {fee:.2f} fee (total: {total:.2f})")
        return True

class PaymentProcessor:
    def __init__(self, method: Optional[PaymentMethod] = None):
        self._method = method

    def set_method(self, method: PaymentMethod) -> None:
        if not isinstance(method, PaymentMethod):
            raise TypeError("Invalid payment method")
        self._method = method

    def process_transaction(self, amount: float) -> bool:
        if self._method is None:
            raise RuntimeError("No payment method selected")
        if amount <= 0:
            raise ValueError("Invalid transaction amount")
        try:
            return self._method.execute_payment(amount)
        except ValueError as e:
            print(f"Payment failed: {e}")
            return False

def main():
    processor = PaymentProcessor()
    
    credit_card = CreditCardPayment()
    processor.set_method(credit_card)
    success = processor.process_transaction(100.0)
    print(f"Transaction successful: {success}\n")
    
    paypal = PayPalPayment()
    processor.set_method(paypal)
    success = processor.process_transaction(200.0)
    print(f"Transaction successful: {success}\n")
    
    processor.set_method(credit_card)
    try:
        success = processor.process_transaction(-50.0)
    except ValueError as e:
        print(f"Error: {e}\n")
    
    try:
        processor.process_transaction(15000.0)
    except ValueError as e:
        print(f"Error: {e}\n")
    
    processor.set_method(paypal)
    try:
        processor.process_transaction(2000.0)
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()