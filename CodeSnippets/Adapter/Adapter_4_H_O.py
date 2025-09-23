import abc
import json
import threading
from typing import Callable, Dict, Any, Optional, Tuple

class ServiceInterface(abc.ABC):
    @abc.abstractmethod
    def execute(self, data: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError

class LegacyProcessor:
    def process(self, payload: str) -> str:
        parts = [p for p in payload.split(";") if p]
        data = {}
        for p in parts:
            if "=" in p:
                k, v = p.split("=", 1)
                data[k] = v
        numeric = [float(v) for v in data.values() if _is_number(v)]
        if numeric:
            return f"result=sum:{sum(numeric)};count:{len(numeric)}"
        return f"result=items:{len(data)};keys:{','.join(sorted(data.keys()))}"

def _is_number(s: str) -> bool:
    try:
        float(s)
        return True
    except Exception:
        return False

class LegacyWrapper(ServiceInterface):
    def __init__(
        self,
        legacy_obj: Any,
        request_serializer: Optional[Callable[[Dict[str, Any]], str]] = None,
        response_parser: Optional[Callable[[str], Dict[str, Any]]] = None,
        cache_enabled: bool = False,
        cache_size: int = 256
    ):
        self._legacy = legacy_obj
        self._serialize = request_serializer or self._default_serialize
        self._parse = response_parser or self._default_parse
        self._cache_enabled = cache_enabled
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._lock = threading.RLock()
        self._cache_size = max(1, cache_size)

    def execute(self, data: Dict[str, Any]) -> Dict[str, Any]:
        if not isinstance(data, dict):
            raise TypeError("data must be a dict")
        key = self._cache_key(data)
        if self._cache_enabled:
            with self._lock:
                if key in self._cache:
                    return dict(self._cache[key])
        payload = self._serialize(data)
        if not hasattr(self._legacy, "process"):
            raise AttributeError("legacy object missing expected 'process' method")
        raw = self._legacy.process(payload)
        result = self._parse(raw)
        if self._cache_enabled:
            with self._lock:
                if len(self._cache) >= self._cache_size:
                    oldest = next(iter(self._cache))
                    del self._cache[oldest]
                self._cache[key] = dict(result)
        return result

    def _cache_key(self, data: Dict[str, Any]) -> str:
        try:
            return json.dumps(data, sort_keys=True, default=str)
        except Exception:
            return str(sorted(data.items()))

    def _default_serialize(self, data: Dict[str, Any]) -> str:
        parts = []
        for k, v in data.items():
            parts.append(f"{k}={v}")
        return ";".join(parts)

    def _default_parse(self, raw: str) -> Dict[str, Any]:
        result = {}
        for part in [p for p in raw.split(";") if p]:
            if ":" in part:
                k, v = part.split(":", 1)
                result[k] = _coerce_value(v)
            elif "=" in part:
                k, v = part.split("=", 1)
                result[k] = _coerce_value(v)
        return result

def _coerce_value(v: str) -> Any:
    if v.isdigit():
        return int(v)
    try:
        f = float(v)
        return f
    except Exception:
        return v

class MethodForwarder(ServiceInterface):
    def __init__(
        self,
        target_obj: Any,
        method_map: Dict[str, str],
        transform_request: Optional[Callable[[Dict[str, Any]], Tuple[Any, ...]]] = None,
        transform_response: Optional[Callable[[Any], Dict[str, Any]]] = None
    ):
        self._target = target_obj
        self._method_map = dict(method_map)
        self._transform_request = transform_request or self._tuple_from_dict
        self._transform_response = transform_response or self._dict_from_any

    def execute(self, data: Dict[str, Any]) -> Dict[str, Any]:
        if "execute" not in self._method_map:
            raise KeyError("method_map must contain 'execute' mapping")
        method_name = self._method_map["execute"]
        if not hasattr(self._target, method_name):
            raise AttributeError(f"target missing method '{method_name}'")
        method = getattr(self._target, method_name)
        args = self._transform_request(data)
        raw = method(*args)
        return self._transform_response(raw)

    def _tuple_from_dict(self, data: Dict[str, Any]) -> Tuple[Any, ...]:
        return (data,)

    def _dict_from_any(self, raw: Any) -> Dict[str, Any]:
        if isinstance(raw, dict):
            return raw
        return {"result": raw}

class OldSensor:
    def fetch(self, config: Dict[str, Any]) -> bytes:
        payload = {"status": "ok", "requested": list(config.keys())}
        return json.dumps(payload).encode("utf-8")

if __name__ == "__main__":
    legacy = LegacyProcessor()
    wrapper = LegacyWrapper(legacy_obj=legacy, cache_enabled=True, cache_size=4)
    input1 = {"a": "1", "b": "2"}
    out1 = wrapper.execute(input1)
    out2 = wrapper.execute(input1)
    sensor = OldSensor()
    forwarder = MethodForwarder(
        target_obj=sensor,
        method_map={"execute": "fetch"},
        transform_request=lambda d: (d,),
        transform_response=lambda b: json.loads(b.decode("utf-8"))
    )
    sensor_result = forwarder.execute({"mode": "fast", "threshold": 0.5})
    print("legacy result:", out1)
    print("cached hit equals:", out1 == out2)
    print("sensor result:", sensor_result)