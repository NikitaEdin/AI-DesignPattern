import random
import time
import uuid

class PaymentError(Exception):
    pass

class PaymentProcessor:
    def process(self, amount: float, currency: str = "USD", idempotency_key: str = None) -> str:
        raise NotImplementedError

class LegacyPaymentGateway:
    def make_payment(self, amount_in_cents: int, currency: str) -> dict:
        if amount_in_cents <= 0:
            raise ValueError("Amount must be positive")
        if random.random() < 0.25:
            raise RuntimeError("Temporary network failure")
        txn_id = str(uuid.uuid4())
        return {"status": "success", "transaction_id": txn_id, "amount": amount_in_cents, "currency": currency}

class PaymentGatewayWrapper(PaymentProcessor):
    def __init__(self, legacy_gateway: LegacyPaymentGateway, retries: int = 3, default_currency: str = "USD"):
        self._legacy = legacy_gateway
        self._retries = max(1, int(retries))
        self._default_currency = default_currency
        self._completed = {}
    def process(self, amount: float, currency: str = None, idempotency_key: str = None) -> str:
        if amount is None or not isinstance(amount, (int, float)):
            raise PaymentError("Invalid amount type")
        if amount <= 0:
            raise PaymentError("Amount must be greater than zero")
        currency = currency or self._default_currency
        key = idempotency_key or f"{amount:.2f}:{currency}"
        if key in self._completed:
            return self._completed[key]
        cents = int(round(amount * 100))
        last_exception = None
        for attempt in range(1, self._retries + 1):
            try:
                result = self._legacy.make_payment(cents, currency)
                if not result or result.get("status") != "success":
                    raise PaymentError("Payment gateway returned failure")
                txn_id = result.get("transaction_id") or str(uuid.uuid4())
                self._completed[key] = txn_id
                return txn_id
            except Exception as exc:
                last_exception = exc
                if attempt < self._retries:
                    time.sleep(0.1 * attempt)
                    continue
                raise PaymentError(f"Payment failed after {self._retries} attempts: {exc}") from exc

if __name__ == "__main__":
    gateway = LegacyPaymentGateway()
    processor = PaymentGatewayWrapper(gateway, retries=4)
    try:
        txn1 = processor.process(12.34)
        print("Transaction 1 ID:", txn1)
        txn2 = processor.process(12.34)
        print("Transaction 2 (idempotent) ID:", txn2)
        txn3 = processor.process(5.00, currency="EUR", idempotency_key="order-123")
        print("Transaction 3 ID:", txn3)
    except PaymentError as e:
        print("Payment error:", e)