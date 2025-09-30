from abc import ABC, abstractmethod
import random

class Transport(ABC):
    @abstractmethod
    def move(self, distance: int) -> str:
        pass

class Car(Transport):
    def __init__(self, fuel: int = 100):
        self.fuel = fuel
    def move(self, distance: int) -> str:
        if self.fuel < distance * 0.05:
            raise ValueError("Insufficient fuel")
        self.fuel -= distance * 0.05
        return f"Car traveled {distance} km, {self.fuel:.1f} fuel left"

class Bike(Transport):
    def __init__(self, gears: int = 5):
        self.gears = gears
    def move(self, distance: int) -> str:
        return f"Bike shifted to gear {min(self.gears, distance//10+1)} and cycled {distance} km"

class Drone(Transport):
    def __init__(self, battery: int = 100):
        self.battery = battery
    def move(self, distance: int) -> str:
        consumption = distance * 2
        if self.battery < consumption:
            raise ValueError("Battery too low")
        self.battery -= consumption
        return f"Drone flew {distance} km, {self.battery}% battery remains"

class VehicleDispenser:
    _types = {"car": Car, "bike": Bike, "drone": Drone}
    @classmethod
    def create(cls, kind: str, **kwargs) -> Transport:
        if kind not in cls._types:
            raise ValueError("Unknown kind")
        return cls._types[kind](**kwargs)
    @classmethod
    def register(cls, kind: str, vehicle_cls: type):
        if not issubclass(vehicle_cls, Transport):
            raise TypeError("Invalid transport")
        cls._types[kind] = vehicle_cls
    @classmethod
    def list_kinds(cls):
        return list(cls._types.keys())

if __name__ == "__main__":
    random.seed(42)
    vehicles = [
        VehicleDispenser.create("car", fuel=80),
        VehicleDispenser.create("bike", gears=7),
        VehicleDispenser.create("drone", battery=90)
    ]
    for v in vehicles:
        print(v.move(random.randint(10, 100)))
    VehicleDispenser.register("scooter", Bike)
    print(VehicleDispenser.list_kinds())