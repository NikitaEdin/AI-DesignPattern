from __future__ import annotations
from typing import Optional, Protocol, Final
import math

class Engine:
    def __init__(self, horsepower: int, cylinders: int):
        if horsepower <= 0 or cylinders <= 0:
            raise ValueError("Engine specs must be positive")
        self.horsepower = horsepower
        self.cylinders = cylinders

class Chassis:
    def __init__(self, material: str, weight: float):
        if weight <= 0:
            raise ValueError("Weight must be positive")
        self.material = material
        self.weight = weight

class Car:
    def __init__(self, engine: Engine, chassis: Chassis, seats: int, color: str):
        self.engine = engine
        self.chassis = chassis
        self.seats = seats
        self.color = color
    def __repr__(self):
        return (f"Car(engine={self.engine.horsepower}hp/{self.engine.cylinders}cyl, "
                f"chassis={self.chassis.material}/{self.chassis.weight}kg, "
                f"seats={self.seats}, color={self.color})")

class CarSpec(Protocol):
    def set_engine(self, horsepower: int, cylinders: int) -> CarSpec: ...
    def set_chassis(self, material: str, weight: float) -> CarSpec: ...
    def set_seats(self, count: int) -> CarSpec: ...
    def set_color(self, value: str) -> CarSpec: ...
    def create(self) -> Car: ...

class RaceCarImpl:
    _MAX_WEIGHT: Final = 600.0
    def __init__(self):
        self._engine: Optional[Engine] = None
        self._chassis: Optional[Chassis] = None
        self._seats: Optional[int] = None
        self._color: Optional[str] = None
    def set_engine(self, horsepower: int, cylinders: int) -> CarSpec:
        if not 300 <= horsepower <= 1200:
            raise ValueError("Race engine 300-1200 hp")
        self._engine = Engine(horsepower, cylinders)
        return self
    def set_chassis(self, material: str, weight: float) -> CarSpec:
        if weight > self._MAX_WEIGHT:
            raise ValueError(f"Race chassis ≤{self._MAX_WEIGHT}kg")
        self._chassis = Chassis(material, weight)
        return self
    def set_seats(self, count: int) -> CarSpec:
        if count != 1:
            raise ValueError("Race car single seat")
        self._seats = count
        return self
    def set_color(self, value: str) -> CarSpec:
        self._color = value
        return self
    def create(self) -> Car:
        if None in (self._engine, self._chassis, self._seats, self._color):
            raise RuntimeError("Incomplete spec")
        return Car(self._engine, self._chassis, self._seats, self._color)

class FamilyCarImpl:
    _MAX_HORSEPOWER: Final = 400
    def __init__(self):
        self._engine: Optional[Engine] = None
        self._chassis: Optional[Chassis] = None
        self._seats: Optional[int] = None
        self._color: Optional[str] = None
    def set_engine(self, horsepower: int, cylinders: int) -> CarSpec:
        if horsepower > self._MAX_HORSEPOWER:
            raise ValueError("Family engine ≤400 hp")
        self._engine = Engine(horsepower, cylinders)
        return self
    def set_chassis(self, material: str, weight: float) -> CarSpec:
        self._chassis = Chassis(material, weight)
        return self
    def set_seats(self, count: int) -> CarSpec:
        if not 2 <= count <= 9:
            raise ValueError("Family car 2-9 seats")
        self._seats = count
        return self
    def set_color(self, value: str) -> CarSpec:
        self._color = value
        return self
    def create(self) -> Car:
        if None in (self._engine, self._chassis, self._seats, self._color):
            raise RuntimeError("Incomplete spec")
        return Car(self._engine, self._chassis, self._seats, self._color)

if __name__ == "__main__":
    race = RaceCarImpl().set_engine(750, 8).set_chassis("Carbon", 520).set_seats(1).set_color("Red")
    family = FamilyCarImpl().set_engine(180, 4).set_chassis("Steel", 1400).set_seats(5).set_color("Blue")
    print(race.create())
    print(family.create())