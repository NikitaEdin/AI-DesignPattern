from abc import ABC, abstractmethod

class PaymentMethod(ABC):
    @abstractmethod
    def process(self, amount: float) -> bool:
        pass

class CreditCardPayment(PaymentMethod):
    def __init__(self, card_number: str):
        self.card_number = card_number

    def process(self, amount: float) -> bool:
        if not self.card_number or len(self.card_number) < 13:
            return False
        print(f"Processing ${amount} via credit card ending in {self.card_number[-4:]}")
        return True

class BankTransferPayment(PaymentMethod):
    def __init__(self, account_id: str):
        self.account_id = account_id

    def process(self, amount: float) -> bool:
        if not self.account_id:
            return False
        print(f"Processing ${amount} via bank transfer to account {self.account_id}")
        return True

class OrderProcessor:
    def __init__(self, payment_method: PaymentMethod):
        self.payment_method = payment_method

    def set_payment_method(self, payment_method: PaymentMethod):
        self.payment_method = payment_method

    def checkout(self, amount: float) -> bool:
        if amount <= 0:
            print("Invalid amount")
            return False
        return self.payment_method.process(amount)

if __name__ == "__main__":
    processor = OrderProcessor(CreditCardPayment("1234567890123456"))
    processor.checkout(100.0)
    
    processor.set_payment_method(BankTransferPayment("ACC123456"))
    processor.checkout(200.0)