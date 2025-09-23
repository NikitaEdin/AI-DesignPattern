import time
from typing import Any, Dict

class PaymentProcessorInterface:
    def process(self, amount: float) -> Dict[str, Any]:
        raise NotImplementedError

class OldPaySystem:
    def make_payment(self, cents: int) -> Dict[str, Any]:
        if not isinstance(cents, int):
            raise TypeError("cents must be int")
        if cents <= 0:
            raise ValueError("amount must be positive")
        time.sleep(0.1)
        reference = f"OLD-{int(time.time() * 1000)}"
        return {"status": "success", "amount_cents": cents, "reference": reference}

class PaymentBridge(PaymentProcessorInterface):
    def __init__(self, legacy_system: OldPaySystem):
        if not hasattr(legacy_system, "make_payment"):
            raise TypeError("legacy_system must implement make_payment")
        self._legacy = legacy_system
        self._cache: Dict[int, Dict[str, Any]] = {}

    def process(self, amount: float) -> Dict[str, Any]:
        try:
            cents = self._to_cents(amount)
        except Exception as exc:
            return {"status": "error", "message": str(exc)}
        if cents in self._cache:
            result = dict(self._cache[cents])
            result["cached"] = True
            return result
        try:
            result = self._legacy.make_payment(cents)
            if not isinstance(result, dict):
                raise TypeError("unexpected response from legacy system")
            self._cache[cents] = dict(result)
            return result
        except Exception as exc:
            return {"status": "error", "message": f"legacy failure: {exc}"}

    @staticmethod
    def _to_cents(amount: float) -> int:
        if not isinstance(amount, (int, float)):
            raise TypeError("amount must be numeric")
        cents = int(round(float(amount) * 100))
        if cents <= 0:
            raise ValueError("amount must be greater than 0")
        return cents

if __name__ == "__main__":
    legacy = OldPaySystem()
    bridge = PaymentBridge(legacy)
    examples = [10.00, 10.0, 0, "5", 2.345]
    for amt in examples:
        result = bridge.process(amt)
        print(f"Process {amt!r} -> {result}")
    # Demonstrate caching
    r1 = bridge.process(10.00)
    r2 = bridge.process(10.00)
    print("First call reference:", r1.get("reference"))
    print("Second call cached flag:", r2.get("cached", False))