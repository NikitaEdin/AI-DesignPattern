import abc
import random
import time
from typing import Dict, Any


class PaymentError(Exception):
    pass


class PaymentInterface(abc.ABC):
    @abc.abstractmethod
    def process_payment(self, amount: float, currency: str, card_info: Dict[str, Any]) -> Dict[str, Any]:
        pass


class OldPaymentService:
    def make_charge(self, total_cents: int, currency_code: str, card_token: str) -> Dict[str, Any]:
        if random.random() < 0.2:
            raise ConnectionError("temporary network problem")
        if total_cents <= 0:
            return {"result_code": 2, "txn": None, "message": "invalid amount"}
        txn_id = f"OLD-{int(time.time()*1000)}-{random.randint(100,999)}"
        return {"result_code": 0, "txn": txn_id, "charged": total_cents, "currency": currency_code}


class PaymentGatewayWrapper(PaymentInterface):
    def __init__(self, legacy_service: OldPaymentService, max_retries: int = 3, backoff: float = 0.1):
        self._service = legacy_service
        self._max_retries = max_retries
        self._backoff = backoff

    def _validate(self, amount: float, currency: str, card_info: Dict[str, Any]):
        if amount <= 0:
            raise PaymentError("Amount must be positive")
        if not isinstance(currency, str) or len(currency) != 3:
            raise PaymentError("Currency must be a 3-letter code")
        if not card_info.get("token"):
            raise PaymentError("Missing card token")

    def process_payment(self, amount: float, currency: str, card_info: Dict[str, Any]) -> Dict[str, Any]:
        self._validate(amount, currency, card_info)
        total_cents = int(round(amount * 100))
        last_exc = None
        for attempt in range(1, self._max_retries + 1):
            try:
                resp = self._service.make_charge(total_cents, currency.upper(), card_info["token"])
                return self._normalize_response(resp)
            except ConnectionError as exc:
                last_exc = exc
                time.sleep(self._backoff * attempt)
            except Exception as exc:
                raise PaymentError(f"Processing failed: {exc}") from exc
        raise PaymentError(f"Transient error after retries: {last_exc}")

    def _normalize_response(self, resp: Dict[str, Any]) -> Dict[str, Any]:
        code = resp.get("result_code", 1)
        if code == 0:
            return {"status": "success", "transaction_id": resp.get("txn"), "amount": resp.get("charged"), "currency": resp.get("currency")}
        return {"status": "failure", "error": resp.get("message", "unknown"), "transaction_id": resp.get("txn")}


if __name__ == "__main__":
    legacy = OldPaymentService()
    gateway = PaymentGatewayWrapper(legacy, max_retries=4, backoff=0.05)
    card = {"token": "tok_visa_123"}
    try:
        result = gateway.process_payment(12.50, "usd", card)
        print("Payment result:", result)
    except PaymentError as e:
        print("Payment failed:", e)