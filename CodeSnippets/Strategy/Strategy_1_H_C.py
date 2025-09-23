from abc import ABC, abstractmethod
from typing import Any, Dict, Type, Optional
import functools

class PaymentProcessor(ABC):
    @abstractmethod
    def process_payment(self, amount: float, **kwargs) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    def validate_payment_data(self, **kwargs) -> bool:
        pass

class CreditCardProcessor(PaymentProcessor):
    def process_payment(self, amount: float, **kwargs) -> Dict[str, Any]:
        card_number = kwargs.get('card_number', '')
        if not self.validate_payment_data(**kwargs):
            return {'status': 'failed', 'error': 'Invalid card data'}
        return {
            'status': 'success',
            'transaction_id': f'cc_{hash(card_number) % 1000000}',
            'amount': amount,
            'fee': amount * 0.029
        }
    
    def validate_payment_data(self, **kwargs) -> bool:
        card_number = kwargs.get('card_number', '')
        cvv = kwargs.get('cvv', '')
        return len(card_number) == 16 and len(cvv) == 3

class PayPalProcessor(PaymentProcessor):
    def process_payment(self, amount: float, **kwargs) -> Dict[str, Any]:
        email = kwargs.get('email', '')
        if not self.validate_payment_data(**kwargs):
            return {'status': 'failed', 'error': 'Invalid PayPal credentials'}
        return {
            'status': 'success',
            'transaction_id': f'pp_{hash(email) % 1000000}',
            'amount': amount,
            'fee': amount * 0.034
        }
    
    def validate_payment_data(self, **kwargs) -> bool:
        email = kwargs.get('email', '')
        return '@' in email and '.' in email

class CryptoProcessor(PaymentProcessor):
    def process_payment(self, amount: float, **kwargs) -> Dict[str, Any]:
        wallet_address = kwargs.get('wallet_address', '')
        if not self.validate_payment_data(**kwargs):
            return {'status': 'failed', 'error': 'Invalid wallet address'}
        return {
            'status': 'success',
            'transaction_id': f'crypto_{hash(wallet_address) % 1000000}',
            'amount': amount,
            'fee': 0.50
        }
    
    def validate_payment_data(self, **kwargs) -> bool:
        wallet_address = kwargs.get('wallet_address', '')
        return len(wallet_address) >= 26 and wallet_address.startswith(('1', '3', 'bc1'))

class PaymentContext:
    def __init__(self):
        self._processor: Optional[PaymentProcessor] = None
        self._registry: Dict[str, Type[PaymentProcessor]] = {
            'credit_card': CreditCardProcessor,
            'paypal': PayPalProcessor,
            'crypto': CryptoProcessor
        }
    
    def set_processor(self, processor: PaymentProcessor) -> None:
        self._processor = processor
    
    def auto_select_processor(self, payment_method: str) -> bool:
        if payment_method in self._registry:
            self._processor = self._registry[payment_method]()
            return True
        return False
    
    def register_processor(self, name: str, processor_class: Type[PaymentProcessor]) -> None:
        self._registry[name] = processor_class
    
    @functools.wraps(PaymentProcessor.process_payment)
    def execute_payment(self, amount: float, **kwargs) -> Dict[str, Any]:
        if not self._processor:
            return {'status': 'failed', 'error': 'No payment processor configured'}
        
        if amount <= 0:
            return {'status': 'failed', 'error': 'Invalid amount'}
        
        try:
            result = self._processor.process_payment(amount, **kwargs)
            return result
        except Exception as e:
            return {'status': 'failed', 'error': f'Processing error: {str(e)}'}

if __name__ == "__main__":
    payment_context = PaymentContext()
    
    print("Credit Card Payment:")
    payment_context.auto_select_processor('credit_card')
    result1 = payment_context.execute_payment(100.0, card_number='1234567890123456', cvv='123')
    print(f"Result: {result1}")
    
    print("\nPayPal Payment:")
    payment_context.auto_select_processor('paypal')
    result2 = payment_context.execute_payment(250.0, email='user@example.com')
    print(f"Result: {result2}")
    
    print("\nCrypto Payment:")
    payment_context.auto_select_processor('crypto')
    result3 = payment_context.execute_payment(500.0, wallet_address='1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa')
    print(f"Result: {result3}")
    
    print("\nInvalid Payment:")
    result4 = payment_context.execute_payment(75.0, card_number='invalid')
    print(f"Result: {result4}")