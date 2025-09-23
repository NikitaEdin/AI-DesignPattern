import json
import time
import random
import threading
from typing import Callable, Optional, Dict, Any
from abc import ABC, abstractmethod


class RequestHandler(ABC):
    @abstractmethod
    def handle(self, data: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError


class LegacyProcessor:
    def __init__(self, reliability: float = 0.8, latency: float = 0.2):
        self.reliability = max(0.0, min(1.0, reliability))
        self.latency = max(0.0, latency)

    def execute(self, payload: str, encoding: str = "utf-8") -> str:
        time.sleep(self.latency)
        if random.random() > self.reliability:
            raise RuntimeError("legacy failure")
        try:
            obj = json.loads(payload)
        except Exception:
            raise ValueError("invalid payload")
        result = {"status": "ok", "received": obj, "note": "processed_by_legacy"}
        return json.dumps(result, ensure_ascii=False).encode(encoding).decode(encoding)


class ValidationError(Exception):
    pass


class ServiceError(Exception):
    pass


class TranslationError(Exception):
    pass


class ServiceTranslator(RequestHandler):
    def __init__(
        self,
        legacy: LegacyProcessor,
        validator: Optional[Callable[[Dict[str, Any]], Dict[str, Any]]] = None,
        max_retries: int = 3,
        backoff_factor: float = 0.1,
        cache_enabled: bool = True,
    ):
        self._legacy = legacy
        self._validator = validator
        self._max_retries = max(0, int(max_retries))
        self._backoff = max(0.0, backoff_factor)
        self._cache_enabled = bool(cache_enabled)
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._lock = threading.RLock()

    def _serialize(self, data: Dict[str, Any]) -> str:
        try:
            return json.dumps(data, sort_keys=True, ensure_ascii=False)
        except TypeError as e:
            raise ValidationError(f"unserializable payload: {e}") from e

    def _deserialize(self, text: str) -> Dict[str, Any]:
        try:
            return json.loads(text)
        except Exception as e:
            raise TranslationError(f"invalid response from legacy: {e}") from e

    def _call_legacy_with_retry(self, payload: str) -> str:
        attempt = 0
        while True:
            try:
                return self._legacy.execute(payload)
            except Exception as exc:
                attempt += 1
                if attempt > self._max_retries:
                    raise ServiceError(f"service failed after {self._max_retries} retries: {exc}") from exc
                sleep = self._backoff * (2 ** (attempt - 1))
                time.sleep(sleep)

    def handle(self, data: Dict[str, Any]) -> Dict[str, Any]:
        if not isinstance(data, dict):
            raise ValidationError("input must be a dict")
        normalized = data
        if self._validator:
            normalized = self._validator(dict(data))
            if not isinstance(normalized, dict):
                raise ValidationError("validator must return a dict")
        payload = self._serialize(normalized)
        if self._cache_enabled:
            with self._lock:
                cached = self._cache.get(payload)
                if cached is not None:
                    return dict(cached)
        response_text = self._call_legacy_with_retry(payload)
        parsed = self._deserialize(response_text)
        mapped = self._map_response(parsed)
        if self._cache_enabled:
            with self._lock:
                self._cache[payload] = dict(mapped)
        return mapped

    def _map_response(self, parsed: Dict[str, Any]) -> Dict[str, Any]:
        try:
            status = parsed.get("status")
            received = parsed.get("received", {})
            return {"status": status, "echo": received, "meta": {"source": "legacy"}}
        except Exception as e:
            raise TranslationError(f"mapping failed: {e}") from e


if __name__ == "__main__":
    random.seed(0)

    def simple_validator(d: Dict[str, Any]) -> Dict[str, Any]:
        if "value" not in d:
            raise ValidationError("missing 'value'")
        return {"value": d["value"], "timestamp": int(time.time())}

    legacy = LegacyProcessor(reliability=0.6, latency=0.25)
    translator = ServiceTranslator(legacy, validator=simple_validator, max_retries=4, backoff_factor=0.05)

    inputs = [
        {"value": 42},
        {"value": 42},
        {"value": "test"},
        {"no_value": True},
    ]

    for idx, inp in enumerate(inputs, 1):
        start = time.time()
        try:
            result = translator.handle(inp)
            elapsed = time.time() - start
            print(f"#{idx} success ({elapsed:.3f}s): {result}")
        except Exception as e:
            elapsed = time.time() - start
            print(f"#{idx} error ({elapsed:.3f}s): {e}")