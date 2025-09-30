from typing import Optional, List
import json

class Engine:
    def __init__(self, horsepower: int, fuel: str):
        self.horsepower = horsepower
        self.fuel = fuel

class Chassis:
    def __init__(self, material: str, weight: int):
        self.material = material
        self.weight = weight

class Cabin:
    def __init__(self, seats: int, color: str, extras: List[str]):
        self.seats = seats
        self.color = color
        self.extras = extras

class Vehicle:
    def __init__(self, engine: Engine, chassis: Chassis, cabin: Cabin):
        self.engine = engine
        self.chassis = chassis
        self.cabin = cabin

    def __repr__(self):
        return json.dumps({
            "engine": {"horsepower": self.engine.horsepower, "fuel": self.engine.fuel},
            "chassis": {"material": self.chassis.material, "weight": self.chassis.weight},
            "cabin": {"seats": self.cabin.seats, "color": self.cabin.color, "extras": self.cabin.extras}
        }, indent=2)

class VehicleAssembler:
    def __init__(self):
        self._engine: Optional[Engine] = None
        self._chassis: Optional[Chassis] = None
        self._cabin: Optional[Cabin] = None

    def power_unit(self, hp: int, fuel: str) -> "VehicleAssembler":
        if hp <= 0:
            raise ValueError("Horsepower must be positive")
        self._engine = Engine(hp, fuel)
        return self

    def frame(self, material: str, weight: int) -> "VehicleAssembler":
        if weight <= 0:
            raise ValueError("Weight must be positive")
        self._chassis = Chassis(material, weight)
        return self

    def interior(self, seats: int, color: str, extras: Optional[List[str]] = None) -> "VehicleAssembler":
        if seats <= 0:
            raise ValueError("Seats must be positive")
        self._cabin = Cabin(seats, color, extras or [])
        return self

    def construct(self) -> Vehicle:
        if not all([self._engine, self._chassis, self._cabin]):
            raise ValueError("Missing components")
        return Vehicle(self._engine, self._chassis, self._cabin)

if __name__ == "__main__":
    car = VehicleAssembler() \
        .power_unit(320, "petrol") \
        .frame("aluminum", 1200) \
        .interior(4, "black", ["leather", "sunroof"]) \
        .construct()
    print(car)