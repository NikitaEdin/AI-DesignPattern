import abc
from dataclasses import dataclass
from typing import Any, Callable, Dict, Optional, Type

class CreationError(Exception):
    pass

class ProductBase(abc.ABC):
    @abc.abstractmethod
    def operate(self) -> str:
        pass

@dataclass
class AlphaProduct(ProductBase):
    level: int = 1
    name: str = "alpha"

    def operate(self) -> str:
        return f"{self.name}-L{self.level}"

@dataclass
class BetaProduct(ProductBase):
    config: Dict[str, Any]
    name: str = "beta"

    def operate(self) -> str:
        return f"{self.name}-{sorted(self.config.items())}"

CreatorCallable = Callable[..., ProductBase]

class CreatorRegistry:
    def __init__(self) -> None:
        self._registry: Dict[str, Dict[str, Any]] = {}

    def register(self, key: str, *, singleton: bool = False) -> Callable[[CreatorCallable], CreatorCallable]:
        def decorator(creator: CreatorCallable) -> CreatorCallable:
            if key in self._registry:
                raise CreationError(f"Key already registered: {key}")
            self._registry[key] = {"creator": creator, "singleton": singleton, "instance": None}
            return creator
        return decorator

    def register_direct(self, key: str, creator: CreatorCallable, *, singleton: bool = False) -> None:
        if key in self._registry:
            raise CreationError(f"Key already registered: {key}")
        self._registry[key] = {"creator": creator, "singleton": singleton, "instance": None}

    def create(self, key: str, **kwargs: Any) -> ProductBase:
        meta = self._registry.get(key)
        if not meta:
            raise CreationError(f"Unknown product key: {key}")
        if meta["singleton"]:
            if meta["instance"] is not None:
                return meta["instance"]
        creator = meta["creator"]
        try:
            result = creator(**kwargs)
        except TypeError as e:
            raise CreationError(f"Creation failed for {key}: {e}") from e
        if not isinstance(result, ProductBase):
            raise CreationError(f"Creator for {key} did not return ProductBase instance")
        if meta["singleton"]:
            meta["instance"] = result
        return result

    def create_from_config(self, config: Dict[str, Any]) -> ProductBase:
        if "type" not in config:
            raise CreationError("Config missing 'type' key")
        key = config["type"]
        params = config.get("params", {})
        if not isinstance(params, dict):
            raise CreationError("'params' must be a dict")
        return self.create(key, **params)

if __name__ == "__main__":
    registry = CreatorRegistry()

    @registry.register("alpha", singleton=True)
    class AlphaCreator(AlphaProduct):
        pass

    def beta_builder(config: Optional[Dict[str, Any]] = None) -> BetaProduct:
        if config is None:
            config = {}
        if not isinstance(config, dict):
            raise TypeError("config must be a dict")
        return BetaProduct(config=config)

    registry.register_direct("beta", beta_builder, singleton=False)

    a1 = registry.create("alpha", level=5, name="alphaA")
    a2 = registry.create_from_config({"type": "alpha", "params": {"level": 9}})
    b1 = registry.create("beta", config={"x": 1, "y": 2})

    print(a1.operate())
    print(a2.operate())
    print(b1.operate())
    print(a1 is a2)

    try:
        registry.create("unknown")
    except CreationError as e:
        print("Error:", e)

    try:
        registry.create("beta", config="not-a-dict")
    except CreationError as e:
        print("Error:", e)