import abc
import time
import random
from typing import Any, Dict

class PaymentProcessor(abc.ABC):
    @abc.abstractmethod
    def process(self, amount: float) -> Dict[str, Any]:
        pass

class LegacyStripeClient:
    def charge_cents(self, cents: int) -> Dict[str, Any]:
        if cents <= 0:
            raise ValueError("Amount must be positive cents")
        if cents % 37 == 0:
            raise ConnectionError("Temporary gateway failure")
        transaction_id = f"txn_{random.randint(1000,9999)}"
        return {"status": "success", "id": transaction_id, "amount_cents": cents}

class PaymentGatewayConnector(PaymentProcessor):
    def __init__(self, legacy_client: LegacyStripeClient, max_attempts: int = 3, backoff: float = 0.2):
        self._client = legacy_client
        self._max_attempts = max_attempts
        self._backoff = backoff
        self._last_success: Dict[str, Any] = {}

    def process(self, amount: float) -> Dict[str, Any]:
        if not isinstance(amount, (int, float)):
            raise TypeError("Amount must be a number")
        if amount <= 0:
            raise ValueError("Amount must be greater than zero")
        cents = int(round(amount * 100))
        attempt = 0
        while attempt < self._max_attempts:
            try:
                result = self._client.charge_cents(cents)
                self._last_success = {"amount": amount, "result": result, "attempts": attempt + 1}
                return result
            except Exception as exc:
                attempt += 1
                if attempt >= self._max_attempts:
                    raise RuntimeError(f"Payment failed after {attempt} attempts: {exc}") from exc
                time.sleep(self._backoff * attempt)
        raise RuntimeError("Unreachable payment failure")

if __name__ == "__main__":
    random.seed(42)
    legacy = LegacyStripeClient()
    gateway = PaymentGatewayConnector(legacy, max_attempts=4, backoff=0.1)

    amounts = [12.34, 0.0, 37.0, 99.99]
    for amt in amounts:
        try:
            result = gateway.process(amt)
            print(f"Processed ${amt:.2f} -> {result}")
        except Exception as e:
            print(f"Failed to process ${amt:.2f}: {e}")