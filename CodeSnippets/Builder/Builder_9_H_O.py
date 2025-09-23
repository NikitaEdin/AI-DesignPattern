from __future__ import annotations
from dataclasses import dataclass
from threading import RLock
from typing import Optional, Tuple, List


@dataclass(frozen=True)
class House:
    foundation: str
    walls: str
    roof: str
    electrics: Tuple[str, ...]
    features: Tuple[str, ...]


class AssemblerBase:
    def set_foundation(self, spec: str) -> "AssemblerBase":
        raise NotImplementedError

    def set_walls(self, spec: str) -> "AssemblerBase":
        raise NotImplementedError

    def set_roof(self, spec: str) -> "AssemblerBase":
        raise NotImplementedError

    def configure_electrics(self, spec: str) -> "AssemblerBase":
        raise NotImplementedError

    def add_feature(self, feature: str) -> "AssemblerBase":
        raise NotImplementedError

    def construct(self) -> House:
        raise NotImplementedError


class SimpleAssembler(AssemblerBase):
    def __init__(self) -> None:
        self._lock = RLock()
        self._reset_internal()

    def _reset_internal(self) -> None:
        self._foundation: Optional[str] = None
        self._walls: Optional[str] = None
        self._roof: Optional[str] = None
        self._electrics_order: List[str] = []
        self._features_order: List[str] = []
        self._electrics_set = set()
        self._features_set = set()

    def set_foundation(self, spec: str) -> "SimpleAssembler":
        with self._lock:
            self._foundation = spec.strip()
            return self

    def set_walls(self, spec: str) -> "SimpleAssembler":
        with self._lock:
            self._walls = spec.strip()
            return self

    def set_roof(self, spec: str) -> "SimpleAssembler":
        with self._lock:
            self._roof = spec.strip()
            return self

    def configure_electrics(self, spec: str) -> "SimpleAssembler":
        with self._lock:
            key = spec.strip()
            if key and key not in self._electrics_set:
                self._electrics_order.append(key)
                self._electrics_set.add(key)
            return self

    def add_feature(self, feature: str) -> "SimpleAssembler":
        with self._lock:
            key = feature.strip()
            if key and key not in self._features_set:
                self._features_order.append(key)
                self._features_set.add(key)
            return self

    def construct(self) -> House:
        with self._lock:
            if not (self._foundation and self._walls and self._roof):
                missing = [name for name, val in
                           (("foundation", self._foundation), ("walls", self._walls), ("roof", self._roof))
                           if not val]
                raise ValueError(f"Missing required parts: {', '.join(missing)}")
            house = House(
                foundation=self._foundation,
                walls=self._walls,
                roof=self._roof,
                electrics=tuple(self._electrics_order),
                features=tuple(self._features_order),
            )
            self._reset_internal()
            return house


class LuxuryAssembler(SimpleAssembler):
    def set_foundation(self, spec: str) -> "LuxuryAssembler":
        with self._lock:
            super().set_foundation(spec)
            # Only add reinforced-foundation when the spec explicitly mentions reinforcement
            if spec and "reinforced" in spec.lower():
                if "reinforced-foundation" not in self._features_set:
                    self._features_order.append("reinforced-foundation")
                    self._features_set.add("reinforced-foundation")
            return self

    def add_feature(self, feature: str) -> "LuxuryAssembler":
        with self._lock:
            # Luxury versions may promote certain features
            f = feature.strip()
            if not f:
                return self
            promoted = f"luxury-{f}" if f not in ("garden", "garage") else f
            if promoted not in self._features_set:
                self._features_order.append(promoted)
                self._features_set.add(promoted)
            return self

    def configure_electrics(self, spec: str) -> "LuxuryAssembler":
        with self._lock:
            # Ensure premium electrics are labeled
            s = spec.strip()
            premium = f"premium-{s}" if s and not s.startswith("premium-") else s
            if premium and premium not in self._electrics_set:
                self._electrics_order.append(premium)
                self._electrics_set.add(premium)
            return self


class Coordinator:
    def __init__(self, assembler: AssemblerBase) -> None:
        self._assembler = assembler

    def prepare_standard(self, foundation: str, walls: str, roof: str) -> House:
        return (self._assembler
                .set_foundation(foundation)
                .set_walls(walls)
                .set_roof(roof)
                .configure_electrics("basic-wiring")
                .add_feature("standard-insulation")
                .construct())

    def prepare_custom(self, steps: List[tuple]) -> House:
        a = self._assembler
        for method, arg in steps:
            if not hasattr(a, method):
                raise AttributeError(f"Assembler missing method: {method}")
            getattr(a, method)(arg)
        return a.construct()


if __name__ == "__main__":
    simple = SimpleAssembler()
    coord = Coordinator(simple)
    home1 = coord.prepare_standard("concrete-slab", "brick", "tiled")
    print("Simple home:", home1)

    luxury = LuxuryAssembler()
    luxury_coord = Coordinator(luxury)
    # Using custom step sequence to demonstrate luxury behavior
    steps = [
        ("set_foundation", "reinforced-concrete"),
        ("set_walls", "reinforced-brick"),
        ("set_roof", "slate"),
        ("configure_electrics", "smart-wiring"),
        ("add_feature", "spa"),
        ("add_feature", "garage"),
    ]
    home2 = luxury_coord.prepare_custom(steps)
    print("Luxury home:", home2)