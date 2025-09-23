from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional
from abc import ABC, abstractmethod


@dataclass(frozen=True)
class Vehicle:
    model: str
    engine: str
    wheels: int
    color: str
    airbags: bool
    navigation: Optional[str] = None
    extras: dict = field(default_factory=dict)


class VehicleArchitect(ABC):
    @abstractmethod
    def reset(self) -> None:
        ...

    @abstractmethod
    def prepare_engine(self, spec: str) -> VehicleArchitect:
        ...

    @abstractmethod
    def prepare_wheels(self, count: int) -> VehicleArchitect:
        ...

    @abstractmethod
    def paint_color(self, color: str) -> VehicleArchitect:
        ...

    @abstractmethod
    def enable_navigation(self, system: str) -> VehicleArchitect:
        ...

    @abstractmethod
    def add_airbags(self, count: int) -> VehicleArchitect:
        ...

    @abstractmethod
    def finalize(self) -> Vehicle:
        ...


class SedanArchitect(VehicleArchitect):
    def __init__(self, model: str):
        self.model = model
        self._state = {}
        self.reset()

    def reset(self) -> None:
        self._state = {
            "engine": None,
            "wheels": None,
            "color": "white",
            "airbags": 0,
            "navigation": None,
            "extras": {},
        }

    def prepare_engine(self, spec: str) -> SedanArchitect:
        if not spec:
            raise ValueError("Engine specification required")
        self._state["engine"] = spec
        return self

    def prepare_wheels(self, count: int) -> SedanArchitect:
        if count not in (3, 4, 6):
            raise ValueError("Unsupported wheel count")
        self._state["wheels"] = count
        return self

    def paint_color(self, color: str) -> SedanArchitect:
        if not color:
            raise ValueError("Color must be non-empty")
        self._state["color"] = color
        return self

    def enable_navigation(self, system: str) -> SedanArchitect:
        self._state["navigation"] = system or None
        return self

    def add_airbags(self, count: int) -> SedanArchitect:
        if count < 0:
            raise ValueError("Airbag count cannot be negative")
        self._state["airbags"] = count
        return self

    def add_extra(self, key: str, value) -> SedanArchitect:
        self._state["extras"][key] = value
        return self

    def finalize(self) -> Vehicle:
        if not self._state["engine"] or not self._state["wheels"]:
            raise RuntimeError("Incomplete configuration: engine and wheels required")
        vehicle = Vehicle(
            model=self.model,
            engine=self._state["engine"],
            wheels=self._state["wheels"],
            color=self._state["color"],
            airbags=self._state["airbags"] > 0,
            navigation=self._state["navigation"],
            extras=dict(self._state["extras"]),
        )
        self.reset()
        return vehicle


class DirectorManager:
    def __init__(self, architect: VehicleArchitect):
        self.architect = architect

    def construct_basic(self) -> Vehicle:
        self.architect.reset()
        self.architect.prepare_engine("1.6L I4").prepare_wheels(4).paint_color("silver")
        return self.architect.finalize()

    def construct_with_navigation(self, color: str = "black") -> Vehicle:
        self.architect.reset()
        (self.architect.prepare_engine("2.0L I4 Turbo")
         .prepare_wheels(4)
         .paint_color(color)
         .enable_navigation("ProNav v2")
         .add_airbags(6))
        return self.architect.finalize()


if __name__ == "__main__":
    sedan_arch = SedanArchitect("Sedan-X")
    director = DirectorManager(sedan_arch)

    basic = director.construct_basic()
    print(basic)

    full = director.construct_with_navigation("midnight blue")
    print(full)

    custom = (sedan_arch.prepare_engine("3.0L V6")
              .prepare_wheels(4)
              .paint_color("red")
              .enable_navigation("NavPlus")
              .add_airbags(8)
              .add_extra("sunroof", True)
              .finalize())
    print(custom)

    try:
        incomplete = SedanArchitect("Faulty").finalize()
    except RuntimeError as e:
        print("Error:", e)