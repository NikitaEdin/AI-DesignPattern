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
        required_fields = {'card_number', 'cvv', 'expiry_date'}
        return required_fields.issubset(kwargs.keys()) and len(kwargs['card_number']) == 16
    
    def process_payment(self, amount: float, **kwargs) -> Dict[str, Any]:
        if not self.validate_payment_data(**kwargs):
            return {'status': 'failed', 'error': 'Invalid card data'}
        fee = amount * 0.029
        return {
            'status': 'success',
            'transaction_id': f"CC_{hash(kwargs['card_number']) % 10000:04d}",
            'amount': amount,
            'fee': fee,
            'net_amount': amount - fee
        }

class PayPalProcessor(PaymentProcessor):
    def validate_payment_data(self, **kwargs) -> bool:
        return 'email' in kwargs and '@' in kwargs['email']
    
    def process_payment(self, amount: float, **kwargs) -> Dict[str, Any]:
        if not self.validate_payment_data(**kwargs):
            return {'status': 'failed', 'error': 'Invalid PayPal email'}
        fee = amount * 0.034 + 0.30
        return {
            'status': 'success',
            'transaction_id': f"PP_{hash(kwargs['email']) % 10000:04d}",
            'amount': amount,
            'fee': fee,
            'net_amount': amount - fee
        }

class CryptoProcessor(PaymentProcessor):
    def validate_payment_data(self, **kwargs) -> bool:
        return 'wallet_address' in kwargs and len(kwargs['wallet_address']) == 42
    
    def process_payment(self, amount: float, **kwargs) -> Dict[str, Any]:
        if not self.validate_payment_data(**kwargs):
            return {'status': 'failed', 'error': 'Invalid wallet address'}
        fee = 5.0
        return {
            'status': 'success',
            'transaction_id': f"CR_{hash(kwargs['wallet_address']) % 10000:04d}",
            'amount': amount,
            'fee': fee,
            'net_amount': amount - fee
        }

def transaction_logger(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        result = func(self, *args, **kwargs)
        if hasattr(self, '_transaction_log'):
            self._transaction_log.append(result)
        return result
    return wrapper

class PaymentGateway:
    def __init__(self):
        self._processor: PaymentProcessor = None
        self._processors: Dict[str, PaymentProcessor] = {}
        self._transaction_log = []
    
    def register_processor(self, name: str, processor: PaymentProcessor):
        self._processors[name] = processor
    
    def set_processor(self, name: str):
        if name not in self._processors:
            raise ValueError(f"Processor '{name}' not registered")
        self._processor = self._processors[name]
    
    @transaction_logger
    def execute_payment(self, amount: float, **payment_data) -> Dict[str, Any]:
        if not self._processor:
            return {'status': 'failed', 'error': 'No processor selected'}
        return self._processor.process_payment(amount, **payment_data)
    
    def get_transaction_history(self) -> list:
        return self._transaction_log.copy()
    
    def auto_select_processor(self, **payment_data):
        for name, processor in self._processors.items():
            if processor.validate_payment_data(**payment_data):
                self.set_processor(name)
                return name
        raise ValueError("No suitable processor found for the provided data")

if __name__ == "__main__":
    gateway = PaymentGateway()
    
    gateway.register_processor("credit_card", CreditCardProcessor())
    gateway.register_processor("paypal", PayPalProcessor())
    gateway.register_processor("crypto", CryptoProcessor())
    
    payments = [
        (100.0, {"card_number": "1234567890123456", "cvv": "123", "expiry_date": "12/25"}),
        (250.0, {"email": "user@example.com"}),
        (500.0, {"wallet_address": "0x742d35Cc6634C0532925a3b8D9c1De32Db7b20B8"}),
    ]
    
    for amount, data in payments:
        processor_name = gateway.auto_select_processor(**data)
        result = gateway.execute_payment(amount, **data)
        print(f"Processor: {processor_name}")
        print(f"Result: {result}")
        print("-" * 50)
    
    print(f"Total transactions processed: {len(gateway.get_transaction_history())}")