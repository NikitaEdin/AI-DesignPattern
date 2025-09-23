import time
import threading
import random
from typing import Dict
from abc import ABC, abstractmethod

class PaymentGatewayBase(ABC):
    @abstractmethod
    def process_payment(self, order_id: str, amount: float, currency: str) -> Dict:
        pass

class TransientError(Exception):
    pass

class PermanentError(Exception):
    pass

class LegacyPaymentService:
    def __init__(self, fail_times: int = 0, supported_currencies=None):
        if supported_currencies is None:
            supported_currencies = {"USD", "EUR"}
        self._supported = set(supported_currencies)
        self._fail_times = fail_times
        self._lock = threading.Lock()
        self._call_count = 0

    def send(self, amount_cents: int, currency_code: str, metadata: Dict) -> Dict:
        with self._lock:
            self._call_count += 1
            call_no = self._call_count
        if currency_code not in self._supported:
            raise PermanentError(f"currency_not_supported:{currency_code}")
        if call_no <= self._fail_times:
            if random.random() < 0.8:
                raise TransientError("temporary_network_issue")
        if random.random() < 0.03:
            raise PermanentError("internal_failure")
        transaction_id = f"LEGACY-{int(time.time()*1000)}-{call_no}"
        return {"status_code": 200, "tx": transaction_id, "meta": metadata}

class GatewayBridge(PaymentGatewayBase):
    def __init__(self, service: LegacyPaymentService, max_retries: int = 3, backoff_factor: float = 0.25, max_per_minute: int = 120):
        self._service = service
        self._max_retries = max_retries
        self._backoff = float(backoff_factor)
        self._max_per_minute = max_per_minute
        self._timestamps = []
        self._lock = threading.Lock()

    def _enforce_rate(self):
        now = time.time()
        window_start = now - 60
        with self._lock:
            self._timestamps = [t for t in self._timestamps if t > window_start]
            if len(self._timestamps) >= self._max_per_minute:
                raise TransientError("rate_limit_exceeded")
            self._timestamps.append(now)

    def _map_response(self, legacy_resp: Dict) -> Dict:
        if not isinstance(legacy_resp, dict):
            return {"status": "failed", "reason": "invalid_response", "raw": legacy_resp}
        code = legacy_resp.get("status_code", 500)
        if code == 200:
            return {"status": "success", "transaction_id": legacy_resp.get("tx"), "raw": legacy_resp}
        return {"status": "failed", "reason": f"legacy_status_{code}", "raw": legacy_resp}

    def process_payment(self, order_id: str, amount: float, currency: str) -> Dict:
        if not isinstance(order_id, str) or not order_id.strip():
            raise ValueError("order_id must be a non-empty string")
        if not isinstance(amount, (int, float)) or amount <= 0:
            raise ValueError("amount must be a positive number")
        if not isinstance(currency, str) or len(currency) != 3:
            raise ValueError("currency must be a 3-letter code")
        amount_cents = int(round(amount * 100))
        metadata = {"order_id": order_id, "submitted_at": time.time()}
        attempt = 0
        while True:
            attempt += 1
            try:
                self._enforce_rate()
                resp = self._service.send(amount_cents, currency.upper(), metadata)
                return self._map_response(resp)
            except TransientError as te:
                if attempt > self._max_retries:
                    return {"status": "failed", "reason": "transient_retry_exhausted", "error": str(te)}
                sleep_for = self._backoff * (2 ** (attempt - 1))
                time.sleep(sleep_for)
                continue
            except PermanentError as pe:
                return {"status": "failed", "reason": "permanent_error", "error": str(pe)}
            except Exception as ex:
                return {"status": "failed", "reason": "unexpected_error", "error": str(ex)}

if __name__ == "__main__":
    legacy = LegacyPaymentService(fail_times=2, supported_currencies={"USD", "EUR", "GBP"})
    gateway = GatewayBridge(legacy, max_retries=4, backoff_factor=0.1, max_per_minute=10)

    orders = [
        ("order-1001", 19.99, "USD"),
        ("order-1002", 5.50, "EUR"),
        ("order-1003", 12.00, "JPY"),
        ("order-1004", -3.00, "USD"),
    ]

    for oid, amt, cur in orders:
        try:
            result = gateway.process_payment(oid, amt, cur)
        except Exception as e:
            result = {"status": "failed", "reason": "validation_error", "error": str(e)}
        print(f"{oid} -> {result}")