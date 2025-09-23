from __future__ import annotations
from dataclasses import dataclass, asdict, field
from typing import Dict, List, Any
from abc import ABC, abstractmethod
import copy
import sys


class ConstructionError(Exception):
    pass


@dataclass(frozen=True)
class Product:
    model: str
    parts: Dict[str, Any]
    size: int
    features: List[str]


class AbstractAssembler(ABC):
    @abstractmethod
    def set_model(self, model: str) -> "AbstractAssembler":
        raise NotImplementedError

    @abstractmethod
    def add_part(self, key: str, value: Any) -> "AbstractAssembler":
        raise NotImplementedError

    @abstractmethod
    def set_size(self, size: int) -> "AbstractAssembler":
        raise NotImplementedError

    @abstractmethod
    def add_feature(self, feature: str) -> "AbstractAssembler":
        raise NotImplementedError

    @abstractmethod
    def assemble(self) -> Product:
        raise NotImplementedError

    @abstractmethod
    def reset(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def clone(self) -> "AbstractAssembler":
        raise NotImplementedError


class CompactAssembler(AbstractAssembler):
    def __init__(self) -> None:
        self.reset()

    def set_model(self, model: str) -> "CompactAssembler":
        if not model or not model.strip():
            raise ConstructionError("Model name must be non-empty.")
        self._state["model"] = model.strip()
        return self

    def add_part(self, key: str, value: Any) -> "CompactAssembler":
        if not key or not isinstance(key, str):
            raise ConstructionError("Part key must be a valid string.")
        if value is None:
            raise ConstructionError("Part value cannot be None.")
        self._state["parts"][key] = value
        return self

    def set_size(self, size: int) -> "CompactAssembler":
        if not isinstance(size, int) or size <= 0:
            raise ConstructionError("Size must be a positive integer.")
        self._state["size"] = size
        return self

    def add_feature(self, feature: str) -> "CompactAssembler":
        if not feature or not isinstance(feature, str):
            raise ConstructionError("Feature must be a non-empty string.")
        self._state["features"].append(feature)
        return self

    def assemble(self) -> Product:
        if self._assembled:
            raise ConstructionError("Current configuration has already been assembled; reset to reuse.")
        if "model" not in self._state or not self._state["model"]:
            raise ConstructionError("Model is required before assembly.")
        if not self._state["parts"]:
            raise ConstructionError("At least one part is required.")
        if "size" not in self._state:
            self._state["size"] = max(1, sum(1 for _ in self._state["parts"]) )
        product = Product(
            model=self._state["model"],
            parts=copy.deepcopy(self._state["parts"]),
            size=int(self._state["size"]),
            features=list(self._state["features"]),
        )
        self._assembled = True
        return product

    def reset(self) -> None:
        self._state = {"model": "", "parts": {}, "size": 0, "features": []}
        self._assembled = False

    def clone(self) -> "CompactAssembler":
        cloned = CompactAssembler()
        cloned._state = copy.deepcopy(self._state)
        cloned._assembled = self._assembled
        return cloned


class LuxuryAssembler(CompactAssembler):
    def add_part(self, key: str, value: Any) -> "LuxuryAssembler":
        super().add_part(key, value)
        return self

    def add_feature(self, feature: str) -> "LuxuryAssembler":
        super().add_feature(feature)
        return self

    def assemble(self) -> Product:
        if self._assembled:
            raise ConstructionError("Current configuration has already been assembled; reset to reuse.")
        if "model" not in self._state or not self._state["model"]:
            raise ConstructionError("Model is required before assembly.")
        if "engine" not in self._state["parts"]:
            raise ConstructionError("Luxury configuration requires an engine part.")
        if "premium_interior" not in self._state["features"]:
            self._state["features"].append("premium_interior")
        if self._state.get("size", 0) < 2:
            self._state["size"] = max(2, len(self._state["parts"]))
        product = Product(
            model=self._state["model"],
            parts=copy.deepcopy(self._state["parts"]),
            size=int(self._state["size"]),
            features=list(self._state["features"]),
        )
        self._assembled = True
        return product

    def clone(self) -> "LuxuryAssembler":
        cloned = LuxuryAssembler()
        cloned._state = copy.deepcopy(self._state)
        cloned._assembled = self._assembled
        return cloned


class Coordinator:
    def assemble_minimal(self, assembler: AbstractAssembler, model: str) -> Product:
        assembler.reset()
        assembler.set_model(model)
        assembler.add_part("chassis", {"material": "steel"})
        try:
            return assembler.assemble()
        except ConstructionError as e:
            raise

    def assemble_full(self, assembler: AbstractAssembler, model: str) -> Product:
        assembler.reset()
        assembler.set_model(model)
        assembler.set_size(4)
        assembler.add_part("chassis", {"material": "aluminum"})
        assembler.add_part("engine", {"type": "V8"})
        assembler.add_part("wheels", 4)
        assembler.add_feature("navigation")
        assembler.add_feature("climate_control")
        return assembler.assemble()

    def assemble_custom(self, assembler: AbstractAssembler, spec: Dict[str, Any]) -> Product:
        assembler.reset()
        if "model" in spec:
            assembler.set_model(spec["model"])
        for k, v in spec.get("parts", {}).items():
            assembler.add_part(k, v)
        if "size" in spec:
            assembler.set_size(int(spec["size"]))
        for f in spec.get("features", []):
            assembler.add_feature(f)
        return assembler.assemble()


if __name__ == "__main__":
    coord = Coordinator()
    compact = CompactAssembler()
    luxury = LuxuryAssembler()

    try:
        p1 = coord.assemble_minimal(compact, "EconoX")
        print(asdict(p1))
    except ConstructionError as e:
        print("Error:", e, file=sys.stderr)

    try:
        p2 = coord.assemble_full(luxury, "Luxor")
        print(asdict(p2))
    except ConstructionError as e:
        print("Error:", e, file=sys.stderr)

    try:
        spec = {
            "model": "CustomOne",
            "parts": {"chassis": {"material": "carbon"}, "engine": {"type": "electric"}, "doors": 2},
            "size": 3,
            "features": ["autopilot"]
        }
        custom_product = coord.assemble_custom(luxury.clone(), spec)
        print(asdict(custom_product))
    except ConstructionError as e:
        print("Error:", e, file=sys.stderr)

    try:
        compact.reset()
        compact.set_model("Faulty")
        compact.set_size(0)
        compact.add_part("sensor", None)
        faulty = compact.assemble()
        print(asdict(faulty))
    except Exception as e:
        print("Expected failure caught:", e, file=sys.stderr)