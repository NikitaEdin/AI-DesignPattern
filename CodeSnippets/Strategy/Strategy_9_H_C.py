from abc import ABC, abstractmethod
from functools import wraps
import time

def performance_monitor(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"{func.__name__} executed in {end - start:.6f} seconds")
        return result
    return wrapper

class PaymentProcessor(ABC):
    @abstractmethod
    def validate_payment(self, amount: float, **kwargs) -> bool:
        pass
    
    @abstractmethod
    def process_transaction(self, amount: float, **kwargs) -> dict:
        pass
    
    @abstractmethod
    def get_processing_fee(self, amount: float) -> float:
        pass

class CreditCardProcessor(PaymentProcessor):
    def __init__(self, max_amount: float = 10000.0):
        self.max_amount = max_amount
    
    def validate_payment(self, amount: float, **kwargs) -> bool:
        card_number = kwargs.get('card_number', '')
        return (amount > 0 and amount <= self.max_amount and 
                len(card_number) == 16 and card_number.isdigit())
    
    @performance_monitor
    def process_transaction(self, amount: float, **kwargs) -> dict:
        if not self.validate_payment(amount, **kwargs):
            return {"status": "failed", "reason": "validation_error"}
        
        time.sleep(0.1)
        return {
            "status": "success",
            "transaction_id": f"CC_{int(time.time())}",
            "fee": self.get_processing_fee(amount),
            "method": "credit_card"
        }
    
    def get_processing_fee(self, amount: float) -> float:
        return amount * 0.029

class BankTransferProcessor(PaymentProcessor):
    def __init__(self, daily_limit: float = 50000.0):
        self.daily_limit = daily_limit
        self.daily_total = 0.0
    
    def validate_payment(self, amount: float, **kwargs) -> bool:
        account_number = kwargs.get('account_number', '')
        return (amount > 0 and self.daily_total + amount <= self.daily_limit and
                len(account_number) >= 8 and account_number.isdigit())
    
    @performance_monitor
    def process_transaction(self, amount: float, **kwargs) -> dict:
        if not self.validate_payment(amount, **kwargs):
            return {"status": "failed", "reason": "validation_error"}
        
        time.sleep(0.2)
        self.daily_total += amount
        return {
            "status": "success",
            "transaction_id": f"BT_{int(time.time())}",
            "fee": self.get_processing_fee(amount),
            "method": "bank_transfer"
        }
    
    def get_processing_fee(self, amount: float) -> float:
        return 5.0 if amount > 1000 else 2.0

class DigitalWalletProcessor(PaymentProcessor):
    def __init__(self, balance: float = 1000.0):
        self.balance = balance
    
    def validate_payment(self, amount: float, **kwargs) -> bool:
        wallet_id = kwargs.get('wallet_id', '')
        return amount > 0 and amount <= self.balance and len(wallet_id) > 0
    
    @performance_monitor
    def process_transaction(self, amount: float, **kwargs) -> dict:
        if not self.validate_payment(amount, **kwargs):
            return {"status": "failed", "reason": "validation_error"}
        
        time.sleep(0.05)
        self.balance -= amount
        return {
            "status": "success",
            "transaction_id": f"DW_{int(time.time())}",
            "fee": self.get_processing_fee(amount),
            "method": "digital_wallet",
            "remaining_balance": self.balance
        }
    
    def get_processing_fee(self, amount: float) -> float:
        return 0.0

class PaymentGateway:
    def __init__(self):
        self._processor = None
    
    def set_processor(self, processor: PaymentProcessor):
        self._processor = processor
    
    def execute_payment(self, amount: float, **kwargs) -> dict:
        if not self._processor:
            return {"status": "failed", "reason": "no_processor_set"}
        
        result = self._processor.process_transaction(amount, **kwargs)
        if result["status"] == "success":
            print(f"Payment of ${amount:.2f} processed successfully via {result['method']}")
        else:
            print(f"Payment failed: {result['reason']}")
        return result

if __name__ == "__main__":
    gateway = PaymentGateway()
    
    cc_processor = CreditCardProcessor()
    bank_processor = BankTransferProcessor()
    wallet_processor = DigitalWalletProcessor(balance=500.0)
    
    payments = [
        (cc_processor, 100.0, {"card_number": "1234567890123456"}),
        (bank_processor, 2500.0, {"account_number": "12345678"}),
        (wallet_processor, 50.0, {"wallet_id": "user123"}),
    ]
    
    for processor, amount, kwargs in payments:
        gateway.set_processor(processor)
        result = gateway.execute_payment(amount, **kwargs)
        print(f"Result: {result}\n")