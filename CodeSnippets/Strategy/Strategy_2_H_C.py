from abc import ABC, abstractmethod
from typing import Dict, Any, Callable
import functools

class PaymentProcessor(ABC):
    @abstractmethod
    def process_payment(self, amount: float, **kwargs) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    def validate_payment_data(self, **kwargs) -> bool:
        pass

class CreditCardProcessor(PaymentProcessor):
    def validate_payment_data(self, **kwargs) -> bool:
        required_fields = ['card_number', 'cvv', 'expiry_date']
        return all(field in kwargs for field in required_fields)
    
    def process_payment(self, amount: float, **kwargs) -> Dict[str, Any]:
        if not self.validate_payment_data(**kwargs):
            return {'status': 'failed', 'error': 'Invalid payment data'}
        
        card_number = kwargs['card_number'][-4:]
        return {
            'status': 'success',
            'transaction_id': f'CC_{hash(card_number + str(amount)) % 100000}',
            'amount': amount,
            'method': 'Credit Card',
            'last_four': card_number
        }

class PayPalProcessor(PaymentProcessor):
    def validate_payment_data(self, **kwargs) -> bool:
        return 'email' in kwargs and '@' in kwargs['email']
    
    def process_payment(self, amount: float, **kwargs) -> Dict[str, Any]:
        if not self.validate_payment_data(**kwargs):
            return {'status': 'failed', 'error': 'Invalid email address'}
        
        return {
            'status': 'success',
            'transaction_id': f'PP_{hash(kwargs["email"] + str(amount)) % 100000}',
            'amount': amount,
            'method': 'PayPal',
            'email': kwargs['email']
        }

class BankTransferProcessor(PaymentProcessor):
    def validate_payment_data(self, **kwargs) -> bool:
        required_fields = ['account_number', 'routing_number']
        return all(field in kwargs for field in required_fields)
    
    def process_payment(self, amount: float, **kwargs) -> Dict[str, Any]:
        if not self.validate_payment_data(**kwargs):
            return {'status': 'failed', 'error': 'Invalid bank details'}
        
        return {
            'status': 'success',
            'transaction_id': f'BT_{hash(kwargs["account_number"] + str(amount)) % 100000}',
            'amount': amount,
            'method': 'Bank Transfer',
            'processing_time': '1-3 business days'
        }

def retry_on_failure(max_retries: int = 3):
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                result = func(*args, **kwargs)
                if result['status'] == 'success':
                    return result
            return {'status': 'failed', 'error': 'Max retries exceeded'}
        return wrapper
    return decorator

class PaymentContext:
    def __init__(self):
        self._processor: PaymentProcessor = None
        self._processors: Dict[str, PaymentProcessor] = {}
    
    def register_processor(self, name: str, processor: PaymentProcessor):
        self._processors[name] = processor
    
    def set_processor(self, processor_name: str):
        if processor_name not in self._processors:
            raise ValueError(f"Processor '{processor_name}' not registered")
        self._processor = self._processors[processor_name]
    
    @retry_on_failure(max_retries=2)
    def execute_payment(self, amount: float, **kwargs) -> Dict[str, Any]:
        if not self._processor:
            return {'status': 'failed', 'error': 'No processor selected'}
        return self._processor.process_payment(amount, **kwargs)
    
    def get_available_processors(self) -> list:
        return list(self._processors.keys())

if __name__ == "__main__":
    context = PaymentContext()
    
    context.register_processor("credit_card", CreditCardProcessor())
    context.register_processor("paypal", PayPalProcessor())
    context.register_processor("bank_transfer", BankTransferProcessor())
    
    print("Available processors:", context.get_available_processors())
    
    context.set_processor("credit_card")
    result1 = context.execute_payment(100.50, card_number="1234567812345678", cvv="123", expiry_date="12/25")
    print("Credit Card Payment:", result1)
    
    context.set_processor("paypal")
    result2 = context.execute_payment(75.25, email="user@example.com")
    print("PayPal Payment:", result2)
    
    context.set_processor("bank_transfer")
    result3 = context.execute_payment(250.00, account_number="123456789", routing_number="987654321")
    print("Bank Transfer Payment:", result3)
    
    result4 = context.execute_payment(50.00, invalid_data="test")
    print("Failed Payment:", result4)