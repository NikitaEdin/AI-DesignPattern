from typing import Protocol
from dataclasses import dataclass
import time

class PaymentMethod(Protocol):
    def process(self, amount: float) -> str: ...

class CreditCard:
    def __init__(self, card_number: str, expiry: str):
        self.card_number = card_number
        self.expiry = expiry
    def process(self, amount: float) -> str:
        if not self.card_number or len(self.card_number) != 16:
            raise ValueError("Invalid card")
        return f"Charged ${amount} using card ending in {self.card_number[-4:]}"

class PayPal:
    def __init__(self, email: str):
        self.email = email
    def process(self, amount: float) -> str:
        if '@' not in self.email:
            raise ValueError("Invalid email")
        return f"Paid ${amount} via PayPal account {self.email}"

class Bitcoin:
    def __init__(method_self, wallet_id: str): 
        method_self.wallet_id = wallet_id
    def process(method_self, amount: float) -> str:
        if not method_self.wallet_id:
            raise ValueError("Invalid wallet")
        return f"Transferred ${amount} in Bitcoin from {method_self.wallet_id[:8]}..."

class Checkout:
    def __init__(self, payment_method: PaymentMethod):
        self.payment_method = payment_method
    def complete_purchase(self, amount: float, item: str) -> str:
        if amount <= 0:
            raise ValueError("Invalid amount")
        timestamp = time.strftime("%Y-%m-%d %H:%M")
        transaction = self.payment_method.process(amount)
        return f"[{timestamp}] Purchase '{item}' - {transaction}"

def main():
    methods = [
        CreditCard("1234567890123456", "12/25"),
        PayPal("user@example.com"),
        Bitcoin("a1b2c3d4e5f6")
    ]
    for method in methods:
        checkout = Checkout(method)
        print(checkout.complete_purchase(99.99, "Notebook"))
    checkout = Checkout(CreditCard("1234567890123456", "12/25"))
    print(checkout.complete_purchase(49.99, "Book"))

if __name__ == "__main__":
    main()