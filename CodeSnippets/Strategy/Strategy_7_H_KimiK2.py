from abc import ABC, abstractmethod
from typing import List, Any
import statistics

class PaymentMethod(ABC):
    @abstractmethod
    def authorize(self, amount: float) -> bool:
        pass
    
    @abstractmethod
    def finalize(self, transaction_id: str) -> str:
        pass

class CreditCard(PaymentMethod):
    def __init__(self, card_no: str, cvv: str):
        self.card_no = card_no
        self.cvv = cvv
    
    def authorize(self, amount: float) -> bool:
        return len(self.card_no) >= 13 and len(self.cvv) == 3
    
    def finalize(self, transaction_id: str) -> str:
        return f"CC_{transaction_id}"

class DigitalWallet(PaymentMethod):
    def __init__(self, wallet_id: str, pin: str):
        self.wallet_id = wallet_id
        self.pin = pin
    
    def authorize(self, amount: float) -> bool:
        return amount <= 1000 and len(self.pin) == 4
    
    def finalize(self, transaction_id: str) -> str:
        return f"DW_{transaction_id}"

class Crypto(PaymentMethod):
    def __init__(self, wallet_addr: str):
        self.wallet_addr = wallet_addr
    
    def authorize(self, amount: float) -> bool:
        return amount >= 0.0001
    
    def finalize(self, transaction_id: str) -> str:
        return f"CR_{transaction_id}"

class Checkout:
    def __init__(self, payment_method: PaymentMethod):
        self.payment_method = payment_method
    
    def set_payment_method(self, payment_method: PaymentMethod):
        self.payment_method = payment_method
    
    def process(self, items: List[Any]) -> str:
        if not items:
            raise ValueError("Empty cart")
        total = sum(item.get('price', 0) for item in items)
        if not self.payment_method.authorize(total):
            raise RuntimeError("Payment authorization failed")
        return self.payment_method.finalize(f"TXN{hash(total)}")

if __name__ == "__main__":
    cart = [{'name': 'book', 'price': 15.99}, {'name': 'pen', 'price': 2.50}]
    checkout = Checkout(CreditCard('4111111111111', '123'))
    print(checkout.process(cart))
    checkout.set_payment_method(DigitalWallet('user123', '1234'))
    print(checkout.process(cart))