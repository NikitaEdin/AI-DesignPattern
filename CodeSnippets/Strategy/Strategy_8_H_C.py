from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import functools

class PaymentProcessor(ABC):
    @abstractmethod
    def process_payment(self, amount: float, **kwargs) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    def validate_payment_data(self, **kwargs) -> bool:
        pass

class CreditCardProcessor(PaymentProcessor):
    def __init__(self, fee_percentage: float = 2.9):
        self.fee_percentage = fee_percentage
    
    def validate_payment_data(self, **kwargs) -> bool:
        required_fields = {'card_number', 'cvv', 'expiry_date'}
        return required_fields.issubset(kwargs.keys()) and len(kwargs.get('card_number', '')) == 16
    
    def process_payment(self, amount: float, **kwargs) -> Dict[str, Any]:
        if not self.validate_payment_data(**kwargs):
            return {'status': 'failed', 'error': 'Invalid card data'}
        
        fee = amount * (self.fee_percentage / 100)
        return {
            'status': 'success',
            'transaction_id': f"CC_{hash(kwargs['card_number']) % 10000}",
            'amount': amount,
            'fee': fee,
            'net_amount': amount - fee
        }

class PayPalProcessor(PaymentProcessor):
    def __init__(self, fee_flat: float = 0.30, fee_percentage: float = 2.4):
        self.fee_flat = fee_flat
        self.fee_percentage = fee_percentage
    
    def validate_payment_data(self, **kwargs) -> bool:
        return 'email' in kwargs and '@' in kwargs['email']
    
    def process_payment(self, amount: float, **kwargs) -> Dict[str, Any]:
        if not self.validate_payment_data(**kwargs):
            return {'status': 'failed', 'error': 'Invalid PayPal email'}
        
        fee = self.fee_flat + (amount * self.fee_percentage / 100)
        return {
            'status': 'success',
            'transaction_id': f"PP_{hash(kwargs['email']) % 10000}",
            'amount': amount,
            'fee': fee,
            'net_amount': amount - fee
        }

class CryptoProcessor(PaymentProcessor):
    def __init__(self, network_fee: float = 5.0):
        self.network_fee = network_fee
    
    def validate_payment_data(self, **kwargs) -> bool:
        wallet_address = kwargs.get('wallet_address', '')
        return len(wallet_address) >= 26 and wallet_address.startswith(('1', '3', 'bc1'))
    
    def process_payment(self, amount: float, **kwargs) -> Dict[str, Any]:
        if not self.validate_payment_data(**kwargs):
            return {'status': 'failed', 'error': 'Invalid wallet address'}
        
        return {
            'status': 'success',
            'transaction_id': f"BTC_{hash(kwargs['wallet_address']) % 10000}",
            'amount': amount,
            'fee': self.network_fee,
            'net_amount': amount - self.network_fee
        }

class PaymentGateway:
    def __init__(self):
        self._processors: Dict[str, PaymentProcessor] = {}
        self._default_processor: Optional[str] = None
    
    def register_processor(self, name: str, processor: PaymentProcessor, is_default: bool = False):
        self._processors[name] = processor
        if is_default or not self._default_processor:
            self._default_processor = name
    
    def set_processor(self, name: str):
        if name not in self._processors:
            raise ValueError(f"Processor '{name}' not registered")
        self._default_processor = name
    
    @functools.lru_cache(maxsize=128)
    def get_processor_info(self, name: str) -> str:
        return f"Processor: {name}, Type: {type(self._processors[name]).__name__}"
    
    def process_transaction(self, amount: float, processor_name: Optional[str] = None, **payment_data) -> Dict[str, Any]:
        processor_name = processor_name or self._default_processor
        
        if not processor_name or processor_name not in self._processors:
            return {'status': 'failed', 'error': 'No valid processor available'}
        
        processor = self._processors[processor_name]
        result = processor.process_payment(amount, **payment_data)
        result['processor_used'] = processor_name
        return result

if __name__ == "__main__":
    gateway = PaymentGateway()
    
    gateway.register_processor("credit_card", CreditCardProcessor(fee_percentage=2.5))
    gateway.register_processor("paypal", PayPalProcessor(fee_flat=0.25, fee_percentage=2.2))
    gateway.register_processor("bitcoin", CryptoProcessor(network_fee=3.0))
    
    transactions = [
        (100.0, "credit_card", {"card_number": "1234567890123456", "cvv": "123", "expiry_date": "12/25"}),
        (250.0, "paypal", {"email": "user@example.com"}),
        (500.0, "bitcoin", {"wallet_address": "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"}),
        (75.0, "credit_card", {"card_number": "invalid"}),
    ]
    
    for amount, processor, data in transactions:
        result = gateway.process_transaction(amount, processor, **data)
        print(f"Amount: ${amount}, Processor: {processor}")
        print(f"Status: {result['status']}")
        if result['status'] == 'success':
            print(f"Net Amount: ${result['net_amount']:.2f}, Fee: ${result['fee']:.2f}")
        else:
            print(f"Error: {result['error']}")
        print("-" * 40)