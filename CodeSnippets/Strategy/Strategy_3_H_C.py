from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import functools

class PaymentProcessor(ABC):
    @abstractmethod
    def process(self, amount: float, **kwargs) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    def validate(self, amount: float, **kwargs) -> bool:
        pass

class CreditCardProcessor(PaymentProcessor):
    def validate(self, amount: float, **kwargs) -> bool:
        card_number = kwargs.get('card_number', '')
        return len(card_number) == 16 and amount > 0
    
    def process(self, amount: float, **kwargs) -> Dict[str, Any]:
        if not self.validate(amount, **kwargs):
            raise ValueError("Invalid credit card payment data")
        fee = amount * 0.029
        return {
            'status': 'success',
            'amount': amount,
            'fee': fee,
            'net_amount': amount - fee,
            'method': 'credit_card'
        }

class PayPalProcessor(PaymentProcessor):
    def validate(self, amount: float, **kwargs) -> bool:
        email = kwargs.get('email', '')
        return '@' in email and amount > 0
    
    def process(self, amount: float, **kwargs) -> Dict[str, Any]:
        if not self.validate(amount, **kwargs):
            raise ValueError("Invalid PayPal payment data")
        fee = amount * 0.034 + 0.30
        return {
            'status': 'success',
            'amount': amount,
            'fee': fee,
            'net_amount': amount - fee,
            'method': 'paypal'
        }

class CryptoProcessor(PaymentProcessor):
    def validate(self, amount: float, **kwargs) -> bool:
        wallet = kwargs.get('wallet_address', '')
        return len(wallet) >= 26 and amount > 0
    
    def process(self, amount: float, **kwargs) -> Dict[str, Any]:
        if not self.validate(amount, **kwargs):
            raise ValueError("Invalid crypto payment data")
        fee = amount * 0.01
        return {
            'status': 'success',
            'amount': amount,
            'fee': fee,
            'net_amount': amount - fee,
            'method': 'cryptocurrency'
        }

def retry_on_failure(max_attempts: int = 3):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise e
            return None
        return wrapper
    return decorator

class PaymentGateway:
    def __init__(self):
        self._processor: Optional[PaymentProcessor] = None
        self._processors: Dict[str, PaymentProcessor] = {
            'credit_card': CreditCardProcessor(),
            'paypal': PayPalProcessor(),
            'crypto': CryptoProcessor()
        }
    
    def set_processor(self, method: str) -> None:
        if method not in self._processors:
            raise ValueError(f"Unsupported payment method: {method}")
        self._processor = self._processors[method]
    
    @retry_on_failure(max_attempts=3)
    def execute_payment(self, amount: float, **kwargs) -> Dict[str, Any]:
        if not self._processor:
            raise RuntimeError("No payment processor configured")
        return self._processor.process(amount, **kwargs)
    
    def get_best_processor(self, amount: float) -> str:
        fees = {}
        for method, processor in self._processors.items():
            if method == 'credit_card':
                fees[method] = amount * 0.029
            elif method == 'paypal':
                fees[method] = amount * 0.034 + 0.30
            else:
                fees[method] = amount * 0.01
        return min(fees, key=fees.get)

if __name__ == "__main__":
    gateway = PaymentGateway()
    
    payments = [
        ('credit_card', 100.0, {'card_number': '1234567890123456'}),
        ('paypal', 250.0, {'email': 'user@example.com'}),
        ('crypto', 500.0, {'wallet_address': 'bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh'})
    ]
    
    for method, amount, details in payments:
        gateway.set_processor(method)
        result = gateway.execute_payment(amount, **details)
        print(f"{method}: ${result['net_amount']:.2f} (fee: ${result['fee']:.2f})")
    
    best_method = gateway.get_best_processor(1000.0)
    print(f"Best method for $1000: {best_method}")