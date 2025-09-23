import abc
import threading
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional, Type


class UnknownTypeError(Exception):
    pass


class RegistrationError(Exception):
    pass


class PoolError(Exception):
    pass


@dataclass
class Spec:
    kind: str
    options: Dict[str, Any] = None


class ProcessorBase(abc.ABC):
    def __init__(self, **options: Any) -> None:
        self.options = options or {}

    @abc.abstractmethod
    def process(self, data: Any) -> Any:
        raise NotImplementedError


class TextHandler(ProcessorBase):
    def process(self, data: Any) -> str:
        txt = str(data)
        prefix = self.options.get("prefix", "")
        suffix = self.options.get("suffix", "")
        return f"{prefix}{txt}{suffix}"


class NumberHandler(ProcessorBase):
    def process(self, data: Any) -> float:
        try:
            val = float(data)
        except Exception as exc:
            raise ValueError("Cannot convert to number") from exc
        factor = float(self.options.get("factor", 1.0))
        return val * factor


class Producer:
    def __init__(self, pool_enabled: bool = True, max_pool_per_type: int = 3) -> None:
        self._registry: Dict[str, Type[ProcessorBase]] = {}
        self._lock = threading.RLock()
        self._pools: Dict[str, List[ProcessorBase]] = {}
        self._pool_enabled = pool_enabled
        self._max_pool = max_pool_per_type

    def register(self, key: str, cls: Type[ProcessorBase]) -> None:
        if not issubclass(cls, ProcessorBase):
            raise RegistrationError("Registered class must inherit from ProcessorBase")
        with self._lock:
            if key in self._registry:
                raise RegistrationError(f"Key already registered: {key}")
            self._registry[key] = cls
            if self._pool_enabled:
                self._pools.setdefault(key, [])

    def unregister(self, key: str) -> None:
        with self._lock:
            if key not in self._registry:
                return
            self._registry.pop(key)
            self._pools.pop(key, None)

    def register_decorator(self, key: str) -> Callable[[Type[ProcessorBase]], Type[ProcessorBase]]:
        def decorator(cls: Type[ProcessorBase]) -> Type[ProcessorBase]:
            self.register(key, cls)
            return cls
        return decorator

    def create(self, spec: Spec, reuse: bool = False) -> ProcessorBase:
        key = spec.kind
        with self._lock:
            cls = self._registry.get(key)
            if cls is None:
                raise UnknownTypeError(f"Unknown kind: {key}")
            if reuse and self._pool_enabled:
                pool = self._pools.setdefault(key, [])
                if pool:
                    inst = pool.pop()
                    inst.options = spec.options or {}
                    return inst
            try:
                instance = cls(**(spec.options or {}))
            except TypeError as exc:
                raise RegistrationError("Invalid options for processor") from exc
            return instance

    def release(self, instance: ProcessorBase) -> None:
        if not self._pool_enabled:
            return
        key = None
        with self._lock:
            for k, cls in self._registry.items():
                if isinstance(instance, cls):
                    key = k
                    break
            if key is None:
                raise PoolError("Instance type not managed by producer")
            pool = self._pools.setdefault(key, [])
            if len(pool) >= self._max_pool:
                return
            pool.append(instance)


if __name__ == "__main__":
    producer = Producer(pool_enabled=True, max_pool_per_type=2)
    producer.register("text", TextHandler)
    producer.register("number", NumberHandler)

    s1 = Spec(kind="text", options={"prefix": "[", "suffix": "]"})
    t1 = producer.create(s1)
    print(t1.process("hello"))

    nspec = Spec(kind="number", options={"factor": 2})
    n1 = producer.create(nspec)
    print(n1.process("3.5"))

    # reuse via pool
    t2 = producer.create(s1, reuse=True)
    print(t2.process("world"))
    producer.release(t2)

    t3 = producer.create(s1, reuse=True)
    print(t3.process("again"))
    producer.release(t3)

    # dynamic registration at runtime using decorator
    @producer.register_decorator("upper")
    class UpperHandler(ProcessorBase):
        def process(self, data: Any) -> Any:
            return str(data).upper()

    up = producer.create(Spec(kind="upper"))
    print(up.process("make me loud"))