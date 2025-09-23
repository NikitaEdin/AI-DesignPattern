import abc
import dataclasses
import threading
import difflib
from typing import Callable, Dict, Any, Type
from concurrent.futures import ThreadPoolExecutor


class Product(abc.ABC):
    @abc.abstractmethod
    def operate(self) -> str:
        pass


@dataclasses.dataclass
class JSONProcessor(Product):
    config: Dict[str, Any]

    def operate(self) -> str:
        return f"JSON processed with keys={sorted(self.config.keys())}"


@dataclasses.dataclass
class XMLProcessor(Product):
    version: str = "1.0"

    def operate(self) -> str:
        return f"XML processed with version={self.version}"


@dataclasses.dataclass
class BinaryProcessor(Product):
    mode: str = "rb"
    size_hint: int = 1024

    def operate(self) -> str:
        return f"Binary processed in {self.mode} mode with hint={self.size_hint}"


class ProducerRegistry:
    def __init__(self):
        self._lock = threading.RLock()
        self._registry: Dict[str, Dict[str, Any]] = {}

    def register(self, name: str, creator: Callable[..., Product] | Type[Product], scope: str = "prototype", replace: bool = False):
        if not name or not isinstance(name, str):
            raise ValueError("name must be a non-empty string")
        if scope not in ("prototype", "singleton"):
            raise ValueError("scope must be 'prototype' or 'singleton'")
        with self._lock:
            if name in self._registry and not replace:
                raise KeyError(f"'{name}' is already registered")
            entry = {"creator": creator, "scope": scope, "instance": None}
            self._registry[name] = entry

    def create(self, name: str, **kwargs) -> Product:
        with self._lock:
            entry = self._registry.get(name)
            if entry is None:
                suggestion = self._suggest(name)
                msg = f"Unknown product '{name}'"
                if suggestion:
                    msg += f". Did you mean: {', '.join(suggestion)}"
                raise ValueError(msg)
            if entry["scope"] == "singleton":
                if entry["instance"] is None:
                    entry["instance"] = self._instantiate(entry["creator"], kwargs)
                return entry["instance"]
            return self._instantiate(entry["creator"], kwargs)

    def _instantiate(self, creator: Callable[..., Product] | Type[Product], kwargs: Dict[str, Any]) -> Product:
        if isinstance(creator, type) and issubclass(creator, Product):
            return creator(**kwargs)
        if callable(creator):
            result = creator(**kwargs)
            if not isinstance(result, Product):
                raise TypeError("creator callable must return a Product instance")
            return result
        raise TypeError("creator must be a Product subclass or callable returning Product")

    def list_registered(self):
        with self._lock:
            return list(self._registry.keys())

    def _suggest(self, name: str):
        names = list(self._registry.keys())
        return difflib.get_close_matches(name, names, n=3, cutoff=0.5)


def special_creator(prefix: str = "special", multiplier: int = 1) -> Product:
    class Special(Product):
        def __init__(self, prefix: str, multiplier: int):
            self.prefix = prefix
            self.multiplier = multiplier

        def operate(self) -> str:
            return f"{self.prefix} x{self.multiplier}"

    return Special(prefix, multiplier)


def main():
    registry = ProducerRegistry()
    registry.register("json", JSONProcessor, scope="prototype")
    registry.register("xml", XMLProcessor, scope="singleton")
    registry.register("bin", BinaryProcessor, scope="prototype")
    registry.register("special", special_creator, scope="prototype")

    p1 = registry.create("json", config={"a": 1, "b": 2})
    p2 = registry.create("json", config={"x": 9})
    s1 = registry.create("xml", version="2.0")
    s2 = registry.create("xml")
    sp = registry.create("special", prefix="alpha", multiplier=3)

    print(p1.operate())
    print(p2.operate())
    print(s1.operate())
    print(s2.operate())
    print(sp.operate())

    names = registry.list_registered()
    print("registered:", names)

    try:
        registry.create("jsn")
    except ValueError as e:
        print("error:", e)

    def task(kind: str, **kw):
        obj = registry.create(kind, **kw)
        return id(obj)

    with ThreadPoolExecutor(max_workers=4) as ex:
        futures = [
            ex.submit(task, "xml"),
            ex.submit(task, "xml"),
            ex.submit(task, "json", config={"t": 1}),
            ex.submit(task, "json", config={"u": 2}),
        ]
        ids = [f.result() for f in futures]
        print("instances ids:", ids)


if __name__ == "__main__":
    main()