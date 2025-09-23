from abc import ABC, abstractmethod
from decimal import Decimal, ROUND_HALF_UP
import threading, time, random

class PaymentGateway(ABC):
    @abstractmethod
    def process_payment(self, amount, currency, reference):
        raise NotImplementedError

class LegacyBankService:
    def send_payment(self, amount_cents, currency, reference):
        r = random.random()
        if r < 0.15:
            raise ConnectionError("transient network error")
        if r < 0.35:
            return {"status": "failed", "error": "insufficient_funds"}
        return {"status": "success", "transaction_id": f"TX{random.randint(1000,9999)}"}

class DuplicatePaymentError(Exception):
    pass

class PaymentServiceBridge(PaymentGateway):
    def __init__(self, legacy_service):
        self._legacy = legacy_service
        self._processed = set()
        self._lock = threading.Lock()

    def _to_cents(self, amount):
        d = Decimal(str(amount)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        if d.is_nan() or d.is_infinite() or d <= 0:
            raise ValueError("amount must be a positive finite number")
        cents = int((d * 100).quantize(Decimal("1"), rounding=ROUND_HALF_UP))
        return d, cents

    def process_payment(self, amount, currency, reference, max_retries=3):
        amount_dec, cents = self._to_cents(amount)
        key = (str(amount_dec), currency, reference)
        with self._lock:
            if key in self._processed:
                raise DuplicatePaymentError("duplicate payment detected")
            self._processed.add(key)
        last_error = None
        attempt = 0
        while attempt < max_retries:
            attempt += 1
            try:
                resp = self._legacy.send_payment(cents, currency, reference)
                if resp.get("status") == "success":
                    return {"status": "success", "transaction_id": resp["transaction_id"], "attempts": attempt}
                last_error = RuntimeError(f"non-success response: {resp}")
            except Exception as exc:
                last_error = exc
            time.sleep(0.1 * attempt)
        with self._lock:
            self._processed.discard(key)
        raise RuntimeError("payment failed after retries") from last_error

if __name__ == "__main__":
    random.seed(2)
    bank = LegacyBankService()
    gateway = PaymentServiceBridge(bank)

    try:
        result = gateway.process_payment("19.99", "USD", "order-1001")
        print("Processed:", result)
    except Exception as e:
        print("Error:", type(e).__name__, e)

    try:
        gateway.process_payment("19.99", "USD", "order-1001")
    except DuplicatePaymentError as d:
        print("Duplicate:", d)