from abc import ABC, abstractmethod
from dataclasses import dataclass
from functools import lru_cache
import time
from typing import Optional

class PaymentProcessor(ABC):
    @abstractmethod
    def process(self, amount: float) -> bool:
        pass
    
    @abstractmethod
    def get_fee(self, amount: float) -> float:
        pass

@dataclass
class BankTransferProcessor(PaymentProcessor):
    account: str
    
    @lru_cache(maxsize=128)
    def process(self, amount: float) -> bool:
        time.sleep(0.1)
        return amount > 0 and len(self.account) == 10
    
    def get_fee(self, amount: float) -> float:
        return max(5.0, amount * 0.001)

@dataclass
class CreditCardProcessor(PaymentProcessor):
    card_number: str
    
    def __post_init__(self):
        if not self.card_number.isdigit() or len(self.card_number) != 16:
            raise ValueError("Invalid card number")
    
    @lru_cache(maxsize=128)
    def process(self, amount: float) -> bool:
        time.sleep(0.05)
        return 0 < amount <= 10000
    
    def get_fee(self, amount: float) -> float:
        return amount * 0.029 + 0.3

class CryptoProcessor(PaymentProcessor):
    def __init__(self, wallet_address: str, network_fee: float = 0.0001):
        self.wallet_address = wallet_address
        self.network_fee = network_fee
    
    @lru_cache(maxsize=128)
    def process(self, amount: float) -> bool:
        time.sleep(0.2)
        return amount > 0.001
    
    def get_fee(self, amount: float) -> float:
        return self.network_fee

class Order:
    def __init__(self, amount: float, processor: Optional[PaymentProcessor] = None):
        if amount <= 0:
            raise ValueError("Amount must be positive")
        self.amount = amount
        self.processor = processor
    
    def set_payment_method(self, processor: PaymentProcessor) -> None:
        self.processor = processor
    
    def complete(self) -> bool:
        if not self.processor:
            raise RuntimeError("No payment method set")
        return self.processor.process(self.amount)
    
    def total_cost(self) -> float:
        if not self.processor:
            return self.amount
        return self.amount + self.processor.get_fee(self.amount)

if __name__ == "__main__":
    bank = BankTransferProcessor("1234567890")
    card = CreditCardProcessor("1234567890123456")
    crypto = CryptoProcessor("1A2b3C4d5E6f7G8h")
    
    order = Order(100.0, bank)
    print(order.complete(), order.total_cost())
    
    order.set_payment_method(card)
    print(order.complete(), order.total_cost())
    
    order.set_payment_method(crypto)
    print(order.complete(), order.total_cost())