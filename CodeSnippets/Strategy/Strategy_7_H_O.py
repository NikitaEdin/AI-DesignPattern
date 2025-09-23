import threading
import pickle
import hashlib
import uuid
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Tuple, Iterable


def _hash_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def _serialize(obj: Any) -> bytes:
    try:
        return pickle.dumps(obj, protocol=pickle.HIGHEST_PROTOCOL)
    except Exception:
        return repr(obj).encode("utf-8")


class HandlerBase(ABC):
    def __init__(self) -> None:
        self._instance_id = uuid.uuid4().hex

    def identifier(self) -> str:
        cls = self.__class__.__name__
        state = self._state_signature()
        return f"{cls}:{_hash_bytes(state)}:{self._instance_id}"

    def _state_signature(self) -> bytes:
        try:
            return pickle.dumps(self._serializable_state(), protocol=pickle.HIGHEST_PROTOCOL)
        except Exception:
            return repr(self._serializable_state()).encode("utf-8")

    def _serializable_state(self) -> Any:
        return getattr(self, "__dict__", {}).copy()

    @abstractmethod
    def process(self, data: Any) -> Any:
        raise NotImplementedError()


class AscendingHandler(HandlerBase):
    def process(self, data: Iterable) -> list:
        return sorted(list(data))


class DescendingHandler(HandlerBase):
    def process(self, data: Iterable) -> list:
        return sorted(list(data), reverse=True)


class UniquePreserveHandler(HandlerBase):
    def process(self, data: Iterable) -> list:
        seen = set()
        out = []
        for item in data:
            if item not in seen:
                seen.add(item)
                out.append(item)
        return out


class CompositeHandler(HandlerBase):
    def __init__(self, handlers: Iterable[HandlerBase]) -> None:
        super().__init__()
        self.handlers = list(handlers)

    def _serializable_state(self) -> Any:
        # Represent internal composition by constituent identifiers
        return {"handlers": [h.identifier() for h in self.handlers]}

    def process(self, data: Any) -> Any:
        result = data
        for h in self.handlers:
            result = h.process(result)
        return result


class FaultyHandler(HandlerBase):
    def process(self, data: Any) -> Any:
        raise RuntimeError("intentional failure")


class Processor:
    def __init__(self, handler: Optional[HandlerBase] = None) -> None:
        self._lock = threading.RLock()
        self._handler: Optional[HandlerBase] = handler
        self._fallback: Optional[HandlerBase] = None
        self._cache: Dict[str, Any] = {}

    def set_handler(self, handler: HandlerBase, clear_cache: bool = True) -> None:
        with self._lock:
            self._handler = handler
            if clear_cache:
                self._cache.clear()

    def set_fallback(self, fallback: Optional[HandlerBase]) -> None:
        with self._lock:
            self._fallback = fallback

    def clear_cache(self) -> None:
        with self._lock:
            self._cache.clear()

    def _make_key(self, handler_id: str, data: Any) -> str:
        data_bytes = _serialize(data)
        data_hash = _hash_bytes(data_bytes)
        return f"{handler_id}:{data_hash}"

    def run(self, data: Any) -> Any:
        with self._lock:
            handler = self._handler
            fallback = self._fallback
        if handler is None:
            raise RuntimeError("no handler configured")

        primary_id = handler.identifier()
        primary_key = self._make_key(primary_id, data)

        with self._lock:
            cached = self._cache.get(primary_key)
        if cached is not None:
            return cached

        try:
            result = handler.process(data)
        except Exception:
            if fallback is None:
                raise
            # Try fallback and cache under fallback identity only
            fallback_id = fallback.identifier()
            fallback_key = self._make_key(fallback_id, data)
            with self._lock:
                cached_fb = self._cache.get(fallback_key)
            if cached_fb is not None:
                return cached_fb
            result = fallback.process(data)
            with self._lock:
                self._cache[fallback_key] = result
            return result

        with self._lock:
            self._cache[primary_key] = result
        return result


if __name__ == "__main__":
    p = Processor()

    asc = AscendingHandler()
    desc = DescendingHandler()
    unique = UniquePreserveHandler()
    comp = CompositeHandler([unique, desc])

    p.set_handler(asc)
    data = [3, 1, 2, 3, 2]
    print("asc:", p.run(data))               # sorted ascending, cached

    p.set_handler(comp)                     # clears cache by default
    print("comp:", p.run(data))              # unique then descending

    # Demonstrate fallback usage and caching only under fallback id
    faulty = FaultyHandler()
    p.set_handler(faulty, clear_cache=False)
    p.set_fallback(asc)
    print("fallback (from asc):", p.run(data))

    # Calling again uses cached fallback result (under asc id), not faulty primary
    print("fallback cached:", p.run(data))

    # Change fallback to descending; new fallback result cached separately
    p.set_fallback(desc)
    print("fallback desc:", p.run(data))