from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from functools import wraps
import time

def performance_monitor(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        start_time = time.time()
        result = func(self, *args, **kwargs)
        execution_time = time.time() - start_time
        self._last_execution_time = execution_time
        return result
    return wrapper

class PaymentProcessor(ABC):
    def __init__(self):
        self._last_execution_time = 0.0
        self._transaction_count = 0
    
    @abstractmethod
    def process_payment(self, amount: float, **kwargs) -> Dict[str, Any]:
        pass
    
    @property
    def execution_time(self) -> float:
        return self._last_execution_time
    
    @property
    def transaction_count(self) -> int:
        return self._transaction_count

class CreditCardProcessor(PaymentProcessor):
    @performance_monitor
    def process_payment(self, amount: float, **kwargs) -> Dict[str, Any]:
        self._transaction_count += 1
        card_number = kwargs.get('card_number', '****-****-****-0000')
        fee = amount * 0.029
        if amount > 10000:
            raise ValueError("Credit card limit exceeded")
        return {
            'status': 'success',
            'amount': amount,
            'fee': fee,
            'method': 'credit_card',
            'card': card_number[-4:],
            'transaction_id': f"CC{self._transaction_count:06d}"
        }

class CryptocurrencyProcessor(PaymentProcessor):
    @performance_monitor
    def process_payment(self, amount: float, **kwargs) -> Dict[str, Any]:
        self._transaction_count += 1
        wallet = kwargs.get('wallet_address', 'unknown')
        fee = 0.0001 * amount
        if amount < 0.001:
            raise ValueError("Minimum cryptocurrency amount not met")
        return {
            'status': 'success',
            'amount': amount,
            'fee': fee,
            'method': 'cryptocurrency',
            'wallet': wallet[:8] + '...',
            'transaction_id': f"CR{self._transaction_count:06d}"
        }

class BankTransferProcessor(PaymentProcessor):
    @performance_monitor
    def process_payment(self, amount: float, **kwargs) -> Dict[str, Any]:
        self._transaction_count += 1
        account = kwargs.get('account_number', '000000000')
        fee = 2.50 if amount < 1000 else 0.0
        return {
            'status': 'success',
            'amount': amount,
            'fee': fee,
            'method': 'bank_transfer',
            'account': f"***{account[-3:]}",
            'transaction_id': f"BT{self._transaction_count:06d}"
        }

class PaymentGateway:
    def __init__(self):
        self._processor: Optional[PaymentProcessor] = None
        self._processors: Dict[str, PaymentProcessor] = {
            'credit': CreditCardProcessor(),
            'crypto': CryptocurrencyProcessor(),
            'bank': BankTransferProcessor()
        }
        self._transaction_history: List[Dict[str, Any]] = []
    
    def set_payment_method(self, method: str):
        if method not in self._processors:
            raise ValueError(f"Unsupported payment method: {method}")
        self._processor = self._processors[method]
    
    def process_transaction(self, amount: float, **kwargs) -> Dict[str, Any]:
        if not self._processor:
            raise RuntimeError("No payment method selected")
        
        try:
            result = self._processor.process_payment(amount, **kwargs)
            result['execution_time'] = self._processor.execution_time
            self._transaction_history.append(result)
            return result
        except Exception as e:
            error_result = {
                'status': 'failed',
                'error': str(e),
                'amount': amount,
                'method': type(self._processor).__name__
            }
            self._transaction_history.append(error_result)
            return error_result
    
    def get_processor_stats(self) -> Dict[str, Dict[str, Any]]:
        return {
            name: {
                'transactions': processor.transaction_count,
                'last_execution': processor.execution_time
            }
            for name, processor in self._processors.items()
        }
    
    @property
    def transaction_history(self) -> List[Dict[str, Any]]:
        return self._transaction_history.copy()

if __name__ == "__main__":
    gateway = PaymentGateway()
    
    transactions = [
        ('credit', 150.00, {'card_number': '1234-5678-9012-3456'}),
        ('crypto', 0.05, {'wallet_address': 'bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh'}),
        ('bank', 2500.00, {'account_number': '123456789'}),
        ('credit', 15000.00, {'card_number': '9876-5432-1098-7654'})
    ]
    
    for method, amount, details in transactions:
        gateway.set_payment_method(method)
        result = gateway.process_transaction(amount, **details)
        print(f"{result['method']}: ${amount} - {result['status']}")
        if 'error' in result:
            print(f"  Error: {result['error']}")
        else:
            print(f"  ID: {result['transaction_id']}, Fee: ${result['fee']:.4f}")
    
    print("\nProcessor Statistics:")
    for name, stats in gateway.get_processor_stats().items():
        print(f"{name}: {stats['transactions']} transactions")