import threading
import inspect
import dataclasses
from dataclasses import dataclass
from typing import Any, Callable, Dict
from abc import ABC, abstractmethod

class ProductBase(ABC):
    @abstractmethod
    def perform(self) -> str:
        pass

class Registry:
    def __init__(self):
        self._lock = threading.RLock()
        self._entries: Dict[str, Dict[str, Any]] = {}

    def register(self, key: str, builder: Callable[..., Any], default_params: Dict[str, Any] = None, singleton: bool = False):
        if not callable(builder):
            raise TypeError("builder must be callable")
        if inspect.isclass(builder) and not issubclass(builder, ProductBase):
            raise TypeError("registered classes must subclass ProductBase")
        entry = {
            "builder": builder,
            "defaults": dict(default_params or {}),
            "singleton": bool(singleton),
            "instance": None,
            "lock": threading.RLock(),
        }
        with self._lock:
            self._entries[key] = entry

    def unregister(self, key: str):
        with self._lock:
            self._entries.pop(key, None)

    def create(self, key: str, **kwargs) -> ProductBase:
        with self._lock:
            entry = self._entries.get(key)
            if entry is None:
                raise KeyError(f"no builder registered under key: {key}")
        lock = entry["lock"]
        with lock:
            if entry["singleton"] and entry["instance"] is not None:
                return entry["instance"]
            builder = entry["builder"]
            params = {**entry["defaults"], **kwargs}
            obj = self._invoke_builder(builder, params)
            if not isinstance(obj, ProductBase):
                raise TypeError("builder did not produce a ProductBase instance")
            if entry["singleton"]:
                entry["instance"] = obj
            return obj

    def _invoke_builder(self, builder: Callable[..., Any], params: Dict[str, Any]) -> Any:
        if inspect.isclass(builder):
            cls = builder
            if dataclasses.is_dataclass(cls):
                missing = []
                for f in dataclasses.fields(cls):
                    if not f.init:
                        continue
                    if (f.default is dataclasses.MISSING and
                        f.default_factory is dataclasses.MISSING and
                        f.name not in params):
                        missing.append(f.name)
                if missing:
                    raise ValueError(f"missing required params for {cls.__name__}: {missing}")
            try:
                return cls(**params)
            except TypeError as e:
                raise ValueError(str(e))
        else:
            sig = inspect.signature(builder)
            try:
                sig.bind(**params)
            except TypeError as e:
                raise ValueError(str(e))
            return builder(**params)

@dataclass
class SimpleProduct(ProductBase):
    name: str
    value: int = 0
    def perform(self) -> str:
        return f"SimpleProduct({self.name}) value={self.value}"

class WorkerProduct(ProductBase):
    def __init__(self, label: str, factor: int = 1):
        if not label:
            raise ValueError("label required")
        self.label = label
        self.factor = factor
    def perform(self) -> str:
        return f"WorkerProduct({self.label}) * {self.factor}"

def make_worker(label: str, factor: int = 1) -> ProductBase:
    return WorkerProduct(label, factor)

if __name__ == "__main__":
    reg = Registry()
    reg.register("simple", SimpleProduct, default_params={"value": 10})
    reg.register("worker", make_worker)
    reg.register("singleton", SimpleProduct, default_params={"name": "one"}, singleton=True)

    p1 = reg.create("simple", name="alpha")
    print(p1.perform())

    p2 = reg.create("worker", label="beta", factor=3)
    print(p2.perform())

    s1 = reg.create("singleton")
    s2 = reg.create("singleton")
    print(s1 is s2, s1.perform())

    try:
        reg.create("simple")  # missing required 'name'
    except ValueError as e:
        print("expected error:", e)