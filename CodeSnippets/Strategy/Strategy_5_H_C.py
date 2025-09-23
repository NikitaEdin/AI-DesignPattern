from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from functools import wraps
import time

def performance_monitor(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} executed in {end - start:.4f} seconds")
        return result
    return wrapper

class PaymentProcessor(ABC):
    @abstractmethod
    def validate(self, amount: float, details: Dict[str, Any]) -> bool:
        pass
    
    @abstractmethod
    def calculate_fees(self, amount: float) -> float:
        pass
    
    @abstractmethod
    def process_payment(self, amount: float, details: Dict[str, Any]) -> Dict[str, Any]:
        pass

class CreditCardProcessor(PaymentProcessor):
    def __init__(self, fee_rate: float = 0.029):
        self.fee_rate = fee_rate
    
    def validate(self, amount: float, details: Dict[str, Any]) -> bool:
        required_fields = ['card_number', 'cvv', 'expiry']
        return all(field in details for field in required_fields) and amount > 0
    
    def calculate_fees(self, amount: float) -> float:
        return amount * self.fee_rate
    
    @performance_monitor
    def process_payment(self, amount: float, details: Dict[str, Any]) -> Dict[str, Any]:
        if not self.validate(amount, details):
            return {'status': 'failed', 'error': 'Invalid payment details'}
        
        fees = self.calculate_fees(amount)
        return {
            'status': 'success',
            'amount': amount,
            'fees': fees,
            'net_amount': amount - fees,
            'method': 'credit_card',
            'card_last_four': details['card_number'][-4:]
        }

class PayPalProcessor(PaymentProcessor):
    def __init__(self, fee_rate: float = 0.034):
        self.fee_rate = fee_rate
    
    def validate(self, amount: float, details: Dict[str, Any]) -> bool:
        return 'email' in details and '@' in details['email'] and amount > 0
    
    def calculate_fees(self, amount: float) -> float:
        return amount * self.fee_rate + 0.30
    
    @performance_monitor
    def process_payment(self, amount: float, details: Dict[str, Any]) -> Dict[str, Any]:
        if not self.validate(amount, details):
            return {'status': 'failed', 'error': 'Invalid PayPal details'}
        
        fees = self.calculate_fees(amount)
        return {
            'status': 'success',
            'amount': amount,
            'fees': fees,
            'net_amount': amount - fees,
            'method': 'paypal',
            'email': details['email']
        }

class BankTransferProcessor(PaymentProcessor):
    def __init__(self, fee_rate: float = 0.01):
        self.fee_rate = fee_rate
        self.min_fee = 5.00
    
    def validate(self, amount: float, details: Dict[str, Any]) -> bool:
        required_fields = ['account_number', 'routing_number']
        return all(field in details for field in required_fields) and amount >= 100
    
    def calculate_fees(self, amount: float) -> float:
        return max(amount * self.fee_rate, self.min_fee)
    
    @performance_monitor
    def process_payment(self, amount: float, details: Dict[str, Any]) -> Dict[str, Any]:
        if not self.validate(amount, details):
            return {'status': 'failed', 'error': 'Invalid bank details or amount below $100'}
        
        fees = self.calculate_fees(amount)
        return {
            'status': 'success',
            'amount': amount,
            'fees': fees,
            'net_amount': amount - fees,
            'method': 'bank_transfer',
            'account_last_four': details['account_number'][-4:]
        }

class PaymentGateway:
    def __init__(self):
        self._processors = {}
        self._default_processor = None
    
    def register_processor(self, name: str, processor: PaymentProcessor, is_default: bool = False):
        self._processors[name] = processor
        if is_default or self._default_processor is None:
            self._default_processor = name
    
    def set_processor(self, name: str):
        if name not in self._processors:
            raise ValueError(f"Processor '{name}' not registered")
        self._default_processor = name
    
    def process_payment(self, amount: float, details: Dict[str, Any], processor_name: Optional[str] = None) -> Dict[str, Any]:
        processor_name = processor_name or self._default_processor
        if processor_name not in self._processors:
            return {'status': 'failed', 'error': 'Invalid processor'}
        
        processor = self._processors[processor_name]
        return processor.process_payment(amount, details)

if __name__ == "__main__":
    gateway = PaymentGateway()
    gateway.register_processor("credit_card", CreditCardProcessor())
    gateway.register_processor("paypal", PayPalProcessor())
    gateway.register_processor("bank_transfer", BankTransferProcessor(), is_default=True)
    
    credit_card_details = {
        'card_number': '4532123456789012',
        'cvv': '123',
        'expiry': '12/25'
    }
    
    paypal_details = {'email': 'user@example.com'}
    
    bank_details = {
        'account_number': '1234567890',
        'routing_number': '987654321'
    }
    
    print("Credit Card Payment:")
    result = gateway.process_payment(1000, credit_card_details, "credit_card")
    print(result)
    
    print("\nPayPal Payment:")
    result = gateway.process_payment(500, paypal_details, "paypal")
    print(result)
    
    print("\nBank Transfer Payment (default):")
    result = gateway.process_payment(2000, bank_details)
    print(result)