import sys
from typing import Optional, List

class Vehicle:
    def __init__(self):
        self.engine: Optional[str] = None
        self.wheels: int = 0
        self.seats: int = 0
        self.airbags: bool = False
        self.extras: List[str] = []

    def __str__(self):
        extras = ", ".join(self.extras) if self.extras else "none"
        return (f"Vehicle(engine={self.engine}, wheels={self.wheels}, "
                f"seats={self.seats}, airbags={self.airbags}, extras=[{extras}])")

class VehicleDesigner:
    def reset(self):
        self._vehicle = Vehicle()
        return self

    def with_engine(self, engine: str):
        if engine not in {"V6", "V8", "Electric"}:
            raise ValueError("Unsupported engine type")
        self._vehicle.engine = engine
        return self

    def with_wheels(self, count: int):
        if count < 0 or count > 12:
            raise ValueError("Wheel count must be 0-12")
        self._vehicle.wheels = count
        return self

    def with_seats(self, count: int):
        if count <= 0:
            raise ValueError("Seat count must be positive")
        self._vehicle.seats = count
        return self

    def with_airbags(self, enabled: bool = True):
        self._vehicle.airbags = enabled
        return self

    def add_feature(self, feature: str):
        self._vehicle.extras.append(feature)
        return self

    def assemble(self) -> Vehicle:
        if not self._vehicle.engine:
            raise ValueError("Engine required")
        if self._vehicle.wheels < 2:
            raise ValueError("At least 2 wheels required")
        result = self._vehicle
        self._vehicle = Vehicle()
        return result

class Director:
    def __init__(self, designer: VehicleDesigner):
        self.designer = designer

    def create_sport_car(self) -> Vehicle:
        return (self.designer.reset()
                .with_engine("V8")
                .with_wheels(4)
                .with_seats(2)
                .with_airbags(True)
                .add_feature("GPS")
                .add_feature("Leather seats")
                .assemble())

    def create_electric_suv(self) -> Vehicle:
        return (self.designer.reset()
                .with_engine("Electric")
                .with_wheels(4)
                .with_seats(7)
                .with_airbags(True)
                .add_feature("Panoramic roof")
                .add_feature("Autopilot")
                .assemble())

if __name__ == "__main__":
    designer = VehicleDesigner()
    director = Director(designer)

    sport_car = director.create_sport_car()
    print("Sport car:", sport_car)

    suv = director.create_electric_suv()
    print("Electric SUV:", suv)

    custom = (designer.reset()
              .with_engine("V6")
              .with_wheels(6)
              .with_seats(4)
              .add_feature("Sunroof")
              .assemble())
    print("Custom vehicle:", custom)