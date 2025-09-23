import random
import time
from abc import ABC, abstractmethod

class PaymentProcessor(ABC):
    @abstractmethod
    def process(self, amount: float) -> dict:
        pass

class LegacyBilling:
    def __init__(self):
        self.system_name = "LegacyBillingV1"
    def charge(self, amount_cents: int) -> dict:
        if not isinstance(amount_cents, int):
            raise TypeError("Amount must be integer cents")
        if amount_cents <= 0:
            raise ValueError("Amount must be positive cents")
        if random.random() < 0.2:
            raise ConnectionError("Temporary connection failure")
        transaction_id = f"TX{int(time.time()*1000)}{amount_cents}"
        return {"transaction_id": transaction_id, "amount_cents": amount_cents, "status": "success"}

class PaymentBridge(PaymentProcessor):
    def __init__(self, legacy_system: LegacyBilling, max_retries: int = 3):
        self.legacy = legacy_system
        self.max_retries = max_retries
        self.last_transaction = None
    def process(self, amount: float) -> dict:
        if not isinstance(amount, (int, float)):
            raise TypeError("Amount must be numeric")
        if amount <= 0:
            raise ValueError("Amount must be greater than zero")
        cents = int(round(amount * 100))
        attempt = 0
        while True:
            try:
                result = self.legacy.charge(cents)
                self.last_transaction = result
                return result
            except ConnectionError:
                attempt += 1
                if attempt >= self.max_retries:
                    raise
                time.sleep(0.1)
            except Exception:
                raise

if __name__ == "__main__":
    random.seed(42)
    legacy = LegacyBilling()
    processor = PaymentBridge(legacy, max_retries=4)
    try:
        res = processor.process(12.34)
        print("Processed:", res)
    except Exception as e:
        print("Failed to process payment:", e)
    try:
        res = processor.process(-5)
        print("Processed:", res)
    except Exception as e:
        print("Failed to process payment:", e)
    try:
        res = processor.process("ten")
        print("Processed:", res)
    except Exception as e:
        print("Failed to process payment:", e)