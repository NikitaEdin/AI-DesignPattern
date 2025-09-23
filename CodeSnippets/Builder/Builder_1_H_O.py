from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict, Iterable, Tuple
from abc import ABC, abstractmethod
import copy


@dataclass(frozen=True)
class Product:
    core: str
    feature: str
    extras: Tuple[Tuple[str, Any], ...]
    version: int

    def info(self) -> str:
        extras_str = ", ".join(f"{k}={v!r}" for k, v in self.extras)
        return f"Product(core={self.core!r}, feature={self.feature!r}, extras={{ {extras_str} }}, version={self.version})"


class RecipeProtocol(ABC):
    @abstractmethod
    def start_new(self, core_spec: str) -> "RecipeProtocol":
        raise NotImplementedError

    @abstractmethod
    def add_feature(self, name: str) -> "RecipeProtocol":
        raise NotImplementedError

    @abstractmethod
    def add_extra(self, key: str, value: Any) -> "RecipeProtocol":
        raise NotImplementedError

    @abstractmethod
    def finalize(self) -> Product:
        raise NotImplementedError


class StandardRecipe(RecipeProtocol):
    def __init__(self) -> None:
        self._reset_internal()

    def _reset_internal(self) -> None:
        self._core: str | None = None
        self._feature: str | None = None
        self._extras: Dict[str, Any] = {}
        self._version = 0
        self._sealed = False

    def start_new(self, core_spec: str) -> "StandardRecipe":
        if not isinstance(core_spec, str) or not core_spec.strip():
            raise ValueError("core_spec must be a non-empty string")
        self._reset_internal()
        self._core = core_spec.strip()
        self._version += 1
        return self

    def add_feature(self, name: str) -> "StandardRecipe":
        if self._sealed:
            raise RuntimeError("Cannot modify after finalize; start_new to reset")
        if not isinstance(name, str) or not name.strip():
            raise ValueError("feature name must be a non-empty string")
        self._feature = name.strip()
        return self

    def add_extra(self, key: str, value: Any) -> "StandardRecipe":
        if self._sealed:
            raise RuntimeError("Cannot modify after finalize; start_new to reset")
        if not isinstance(key, str) or not key.strip():
            raise ValueError("extra key must be a non-empty string")
        # Accept None values intentionally; make a shallow copy for safety
        self._extras[key.strip()] = copy.deepcopy(value)
        return self

    def finalize(self) -> Product:
        if self._sealed:
            raise RuntimeError("Product already finalized; start_new to build another")
        if self._core is None:
            raise ValueError("Core specification missing")
        # Provide a default feature if none set
        feature = self._feature or "default-feature"
        extras_items = tuple(sorted(self._extras.items()))
        self._sealed = True
        product = Product(core=self._core, feature=feature, extras=extras_items, version=self._version)
        return product


class AdvancedRecipe(RecipeProtocol):
    def __init__(self) -> None:
        self._reset_internal()

    def _reset_internal(self) -> None:
        self._components: Dict[str, Any] = {}
        self._sequence: list[str] = []
        self._version = 0
        self._sealed = False

    def start_new(self, core_spec: str) -> "AdvancedRecipe":
        if not core_spec or not isinstance(core_spec, str):
            raise ValueError("core_spec must be a non-empty string")
        self._reset_internal()
        self._components["core"] = core_spec.strip()
        self._sequence.append("core")
        self._version += 1
        return self

    def add_feature(self, name: str) -> "AdvancedRecipe":
        if self._sealed:
            raise RuntimeError("Cannot modify after finalize; start_new to reset")
        if "core" not in self._components:
            raise RuntimeError("Start a new product with start_new before adding features")
        self._components["feature"] = name.strip() if name else "advanced-feature"
        self._sequence.append("feature")
        return self

    def add_extra(self, key: str, value: Any) -> "AdvancedRecipe":
        if self._sealed:
            raise RuntimeError("Cannot modify after finalize; start_new to reset")
        if "extras" not in self._components:
            self._components["extras"] = {}
        self._components["extras"][key] = copy.deepcopy(value)
        self._sequence.append(f"extra:{key}")
        return self

    def finalize(self) -> Product:
        if self._sealed:
            raise RuntimeError("Product already finalized; start_new to build another")
        if "core" not in self._components:
            raise ValueError("Core specification missing")
        feature = self._components.get("feature", "advanced-default")
        extras = tuple(sorted(self._components.get("extras", {}).items()))
        self._sealed = True
        return Product(core=self._components["core"], feature=feature, extras=extras, version=self._version)


class Conductor:
    def orchestrate_minimal(self, recipe: RecipeProtocol, core_spec: str) -> Product:
        return recipe.start_new(core_spec).finalize()

    def orchestrate_complete(self, recipe: RecipeProtocol, core_spec: str, feature: str, extras: Iterable[Tuple[str, Any]] = ()) -> Product:
        r = recipe.start_new(core_spec)
        r.add_feature(feature)
        for k, v in extras:
            r.add_extra(k, v)
        return r.finalize()


if __name__ == "__main__":
    conductor = Conductor()

    standard = StandardRecipe()
    p1 = conductor.orchestrate_minimal(standard, "core-v1")
    print(p1.info())

    p2 = conductor.orchestrate_complete(standard, "core-v2", "enhanced", [("color", "red"), ("size", 42)])
    print(p2.info())

    advanced = AdvancedRecipe()
    # fluent manual composition
    p3 = advanced.start_new("alpha").add_feature("pro").add_extra("cache", True).finalize()
    print(p3.info())

    # error handling demonstration
    try:
        advanced.add_feature("should-fail")
    except RuntimeError as e:
        print("Expected error:", e)