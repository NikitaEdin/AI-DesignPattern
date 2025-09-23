import time
import json
import threading
import hashlib
import copy
import random
from collections import OrderedDict
from typing import Any, Callable, Optional, Tuple

class ServiceInterface:
    def execute(self, data: dict) -> Any:
        raise NotImplementedError

class BasicService(ServiceInterface):
    def execute(self, data: dict) -> Any:
        # Simulate work and return a result dependent on input
        time.sleep(0.01)
        return {"result": data.get("value", 0) * 2}

class WrapperBase(ServiceInterface):
    def __init__(self, inner: ServiceInterface, enabled: bool = True):
        self._inner = inner
        self._enabled = enabled

    def execute(self, data: dict) -> Any:
        # By default, delegate to the inner component
        return self._inner.execute(data)

    def __getattr__(self, name):
        return getattr(self._inner, name)

class CacheLayer(WrapperBase):
    def __init__(self, inner: ServiceInterface, maxsize: int = 128, ttl: Optional[float] = 5.0, enabled: bool = True):
        super().__init__(inner, enabled=enabled)
        self._maxsize = maxsize
        self._ttl = ttl
        self._lock = threading.Lock()
        self._store: OrderedDict = OrderedDict()

    def _make_key(self, data: dict) -> str:
        try:
            return json.dumps(data, sort_keys=True, default=str)
        except Exception:
            h = hashlib.sha256(repr(data).encode()).hexdigest()
            return h

    def execute(self, data: dict) -> Any:
        if not self._enabled:
            return super().execute(data)
        key = self._make_key(data)
        now = time.time()
        with self._lock:
            entry = self._store.get(key)
            if entry:
                ts, value = entry
                if self._ttl is None or now - ts < self._ttl:
                    self._store.move_to_end(key)
                    return copy.deepcopy(value)
                else:
                    del self._store[key]
            # cache miss -> compute
        result = super().execute(data)
        with self._lock:
            self._store[key] = (now, copy.deepcopy(result))
            while len(self._store) > self._maxsize:
                self._store.popitem(last=False)
        return result

class RetryLayer(WrapperBase):
    def __init__(self, inner: ServiceInterface, attempts: int = 3, backoff: float = 0.1,
                 retry_on: Tuple[type, ...] = (Exception,), enabled: bool = True):
        super().__init__(inner, enabled=enabled)
        self._attempts = max(1, attempts)
        self._backoff = max(0.0, backoff)
        self._retry_on = retry_on

    def execute(self, data: dict) -> Any:
        if not self._enabled:
            return super().execute(data)
        last_exc = None
        for i in range(1, self._attempts + 1):
            try:
                return super().execute(data)
            except self._retry_on as exc:
                last_exc = exc
                if i == self._attempts:
                    raise
                time.sleep(self._backoff * (2 ** (i - 1)))
        raise last_exc  # pragma: no cover

class ValidateLayer(WrapperBase):
    def __init__(self, inner: ServiceInterface, schema: Optional[Callable[[dict], None]] = None, enabled: bool = True):
        super().__init__(inner, enabled=enabled)
        self._schema = schema

    def execute(self, data: dict) -> Any:
        if not self._enabled:
            return super().execute(data)
        if self._schema:
            self._schema(data)
        return super().execute(data)

class FlakyService(ServiceInterface):
    def __init__(self, fail_rate: float = 0.5, rng: Optional[random.Random] = None):
        self._fail_rate = min(max(fail_rate, 0.0), 1.0)
        self._rng = rng or random.Random()

    def execute(self, data: dict) -> Any:
        if self._rng.random() < self._fail_rate:
            raise RuntimeError("transient failure")
        return {"ok": True, "value": data.get("value")}

def simple_schema(data: dict):
    if "value" not in data:
        raise ValueError("missing value")
    if not isinstance(data["value"], (int, float)):
        raise TypeError("value must be numeric")

if __name__ == "__main__":
    base = FlakyService(fail_rate=0.4, rng=random.Random(1))
    # Compose layers: validation -> retry -> cache -> service
    svc = ValidateLayer(
        RetryLayer(
            CacheLayer(base, maxsize=64, ttl=2.0),
            attempts=4, backoff=0.05, retry_on=(RuntimeError,)
        ),
        schema=simple_schema
    )

    inputs = [{"value": i} for i in [1, 1, 2, 1]]
    for d in inputs:
        try:
            out = svc.execute(d)
            print("IN:", d, "OUT:", out)
        except Exception as e:
            print("IN:", d, "ERR:", type(e).__name__, str(e))