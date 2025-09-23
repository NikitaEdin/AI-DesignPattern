from abc import ABC, abstractmethod
from threading import Lock
import uuid
import time
import random

class PaymentError(Exception):
    pass

class UnsupportedCurrencyError(PaymentError):
    pass

class RemoteServiceError(PaymentError):
    pass

class PaymentProcessor(ABC):
    @abstractmethod
    def process(self, amount: float, currency: str, metadata: dict = None) -> dict:
        pass

class LegacyStripe:
    def charge(self, cents: int, cur: str, token: str = None) -> dict:
        if cents <= 0:
            raise ValueError("amount must be positive")
        if cur not in ("USD", "EUR"):
            raise RuntimeError("currency not supported")
        if random.random() < 0.1:
            raise ConnectionError("transient network")
        return {"outcome": "approved", "id": f"st_{uuid.uuid4().hex}", "amount": cents, "currency": cur}

class AncientPay:
    def send_payment(self, payload: dict) -> dict:
        if payload.get("value", 0) <= 0:
            raise ValueError("invalid value")
        if payload.get("currency") not in ("USD", "GBP"):
            return {"status": "error", "reason": "unsupported currency"}
        if random.random() < 0.15:
            raise TimeoutError("gateway timeout")
        return {"status": "ok", "ref": f"anc_{uuid.uuid4().hex}", "received": payload}

class GatewayWrapper(PaymentProcessor):
    def __init__(self, service, method_name: str = None, request_builder=None, response_parser=None,
                 fallback: 'GatewayWrapper' = None, retries: int = 1, allowed_currencies=None):
        self._service = service
        self._method_name = method_name
        self._request_builder = request_builder or self._default_request_builder
        self._response_parser = response_parser or self._default_response_parser
        self._fallback = fallback
        self._retries = max(1, int(retries))
        self._lock = Lock()
        self._allowed_currencies = set(allowed_currencies) if allowed_currencies else None

    def _get_callable(self):
        if self._method_name:
            target = getattr(self._service, self._method_name, None)
            if not callable(target):
                raise TypeError("service does not expose required method")
            return target
        for name in ("process", "charge", "send_payment", "pay", "make_payment"):
            target = getattr(self._service, name, None)
            if callable(target):
                return target
        raise TypeError("no compatible method found on service")

    def _default_request_builder(self, amount: float, currency: str, metadata: dict):
        cents = int(round(amount * 100))
        return (cents, currency, metadata.get("token") if metadata else None)

    def _default_response_parser(self, raw):
        if isinstance(raw, dict):
            if raw.get("outcome") in ("approved", "success") or raw.get("status") in ("ok",):
                tx = raw.get("id") or raw.get("ref") or raw.get("transaction") or str(uuid.uuid4())
                amt = raw.get("amount") or (raw.get("received") and raw["received"].get("value"))
                cur = raw.get("currency") or (raw.get("received") and raw["received"].get("currency"))
                return {"status": "success", "transaction_id": tx, "amount_cents": int(amt) if amt is not None else None, "currency": cur}
            reason = raw.get("reason") or raw.get("error") or "unknown"
            raise RemoteServiceError(f"service rejected request: {reason}")
        raise RemoteServiceError("unrecognized response format")

    def _validate(self, amount: float, currency: str):
        if amount <= 0:
            raise ValueError("amount must be positive")
        if self._allowed_currencies and currency not in self._allowed_currencies:
            raise UnsupportedCurrencyError(f"currency {currency} not supported by this gateway")

    def process(self, amount: float, currency: str, metadata: dict = None) -> dict:
        metadata = metadata or {}
        self._validate(amount, currency)
        callable_method = self._get_callable()
        args = self._request_builder(amount, currency, metadata)
        attempt = 0
        last_exc = None
        while attempt < self._retries:
            try:
                with self._lock:
                    raw = callable_method(*args) if isinstance(args, (list, tuple)) else callable_method(args)
                parsed = self._response_parser(raw)
                if not parsed.get("transaction_id"):
                    raise RemoteServiceError("missing transaction id")
                return parsed
            except (ConnectionError, TimeoutError) as e:
                last_exc = e
                attempt += 1
                time.sleep(0.1 * attempt)
                continue
            except Exception as e:
                last_exc = e
                break
        if self._fallback:
            return self._fallback.process(amount, currency, metadata)
        raise RemoteServiceError("processing failed") from last_exc

    def __getattr__(self, item):
        attr = getattr(self._service, item, None)
        if attr:
            return attr
        raise AttributeError(item)

if __name__ == "__main__":
    stripe = LegacyStripe()
    ancient = AncientPay()
    stripe_wrapper = GatewayWrapper(
        service=stripe,
        method_name="charge",
        request_builder=lambda a, c, m: (int(round(a*100)), c, m.get("token") if m else None),
        allowed_currencies=("USD", "EUR"),
        retries=2
    )
    ancient_wrapper = GatewayWrapper(
        service=ancient,
        method_name="send_payment",
        request_builder=lambda a, c, m: ({"value": int(round(a*100)), "currency": c, "meta": m or {}}),
        response_parser=lambda r: {"status": "success", "transaction_id": r.get("ref"), "amount_cents": r["received"]["value"], "currency": r["received"]["currency"]} if r.get("status") == "ok" else (_ for _ in ()).throw(RemoteServiceError("ancient rejected")),
        allowed_currencies=("USD", "GBP"),
        retries=1
    )
    primary = GatewayWrapper(service=stripe, method_name="charge", fallback=ancient_wrapper, retries=2, allowed_currencies=("USD",))
    result1 = stripe_wrapper.process(12.34, "USD", {"token": "tok_123"})
    result2 = ancient_wrapper.process(5.00, "GBP", {"note": "test"})
    try:
        result3 = primary.process(3.21, "EUR", {})
    except Exception as e:
        result3 = {"error": str(e)}
    print(result1)
    print(result2)
    print(result3)