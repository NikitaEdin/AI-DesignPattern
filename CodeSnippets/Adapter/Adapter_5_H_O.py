import abc
import json
import threading
import time
from typing import Any, Callable, Dict, Optional


class ServiceInterface(abc.ABC):
    @abc.abstractmethod
    def process(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError

    @abc.abstractmethod
    def status(self) -> str:
        raise NotImplementedError


class LegacyWorker:
    def __init__(self, name: str):
        self.name = name

    def execute(self, payload_bytes: bytes) -> bytes:
        decoded = payload_bytes.decode("utf-8")
        data = json.loads(decoded)
        if "fail" in data:
            raise ValueError("legacy failure")
        result = {"worker": self.name, "handled": data}
        return json.dumps(result).encode("utf-8")

    def health_check(self) -> dict:
        return {"ok": True, "service": self.name}


class AnotherLegacy:
    def __init__(self, id_: int):
        self.id = id_

    def do_job(self, data: dict) -> dict:
        if data.get("error"):
            raise RuntimeError("job error")
        return {"id": self.id, "result": data}

    def ping(self) -> bool:
        return True


class IncompatibleServiceError(Exception):
    pass


class ServiceBridge(ServiceInterface):
    def __init__(
        self,
        adaptee: Any,
        mapping: Optional[Dict[str, str]] = None,
        cache_ttl: Optional[float] = 0.0,
    ):
        self._adaptee = adaptee
        self._mapping = mapping or {}
        self._cache_ttl = float(cache_ttl or 0.0)
        self._cache: Dict[str, Any] = {}
        self._cache_lock = threading.RLock()
        self._validate_mapping()

    def _validate_mapping(self) -> None:
        required = {"process": None, "status": None}
        for target_name in required:
            mapped = self._mapping.get(target_name)
            if not mapped:
                candidates = [n for n in dir(self._adaptee) if callable(getattr(self._adaptee, n))]
                if target_name == "process":
                    pick = next((n for n in ("execute", "do_job", "run") if n in candidates), None)
                else:
                    pick = next((n for n in ("health_check", "ping", "status") if n in candidates), None)
                if pick is None:
                    raise IncompatibleServiceError(f"no callable for '{target_name}' found on adaptee")
                self._mapping[target_name] = pick

    def _cache_key(self, name: str, args: Any, kwargs: Any) -> str:
        return f"{name}:{repr(args)}:{repr(kwargs)}"

    def _get_cached(self, key: str):
        with self._cache_lock:
            entry = self._cache.get(key)
            if not entry:
                return None
            value, expires = entry
            if expires and time.time() > expires:
                del self._cache[key]
                return None
            return value

    def _set_cache(self, key: str, value: Any):
        with self._cache_lock:
            expires = time.time() + self._cache_ttl if self._cache_ttl > 0 else None
            self._cache[key] = (value, expires)

    def process(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        target_name = self._mapping["process"]
        method = getattr(self._adaptee, target_name, None)
        if not callable(method):
            raise IncompatibleServiceError("mapped process is not callable")
        key = self._cache_key("process", payload, {})
        if self._cache_ttl:
            cached = self._get_cached(key)
            if cached is not None:
                return cached
        try:
            if target_name == "execute":
                raw = json.dumps(payload).encode("utf-8")
                out = method(raw)
                result = json.loads(out.decode("utf-8"))
            else:
                out = method(payload) if isinstance(payload, dict) else method(payload)
                result = out if isinstance(out, dict) else {"result": out}
        except Exception as exc:
            raise IncompatibleServiceError(f"service error: {exc}") from exc
        if self._cache_ttl:
            self._set_cache(key, result)
        return result

    def status(self) -> str:
        target_name = self._mapping["status"]
        method = getattr(self._adaptee, target_name, None)
        if not callable(method):
            raise IncompatibleServiceError("mapped status is not callable")
        try:
            out = method()
            if isinstance(out, dict):
                return "OK" if out.get("ok") else "UNHEALTHY"
            if isinstance(out, bool):
                return "OK" if out else "UNHEALTHY"
            return str(out)
        except Exception as exc:
            return f"ERROR: {exc}"


if __name__ == "__main__":
    legacy = LegacyWorker("legacy-1")
    bridge = ServiceBridge(legacy, cache_ttl=1.0)
    payload = {"task": "process", "value": 42}
    print("first:", bridge.process(payload))
    print("second (cached):", bridge.process(payload))
    time.sleep(1.1)
    print("after ttl:", bridge.process(payload))
    print("status:", bridge.status())

    other = AnotherLegacy(7)
    bridge2 = ServiceBridge(other)
    print("other process:", bridge2.process({"x": 1}))
    print("other status:", bridge2.status())

    try:
        bridge.process({"fail": True})
    except Exception as e:
        print("handled error:", type(e).__name__, str(e))