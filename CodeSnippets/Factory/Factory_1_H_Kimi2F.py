from __future__ import annotations
import json
from abc import ABC, abstractmethod
from typing import Dict, Type

class Vehicle(ABC):
    @abstractmethod
    def specs(self) -> Dict[str, str]:
        pass

class Car(Vehicle):
    def specs(self) -> Dict[str, str]:
        return {"type": "Car", "wheels": "4", "capacity": "5"}

class Motorcycle(Vehicle):
    def specs(self) -> Dict[str, str]:
        return {"type": "Motorcycle", "wheels": "2", "capacity": "2"}

class Truck(Vehicle):
    def specs(self) -> Dict[str, str]:
        return {"type": "Truck", "wheels": "6", "capacity": "3"}

class Assembler:
    _registry: Dict[str, Type[Vehicle]] = {}

    @classmethod
    def register(cls, key: str, vehicle_class: Type[Vehicle]) -> None:
        cls._registry[key] = vehicle_class

    @classmethod
    def create(cls, key: str, **config) -> Vehicle:
        vehicle_class = cls._registry.get(key)
        if not vehicle_class:
            raise ValueError(f"Unknown vehicle type: {key}")
        return vehicle_class(**config)

    @classmethod
    def list_types(cls) -> list[str]:
        return list(cls._registry.keys())

Assembler.register("car", Car)
Assembler.register("motorcycle", Motorcycle)
Assembler.register("truck", Truck)

if __name__ == "__main__":
    order_keys = ["car", "motorcycle", "truck", "car"]
    vehicles = [Assembler.create(k) for k in order_keys]
    for v in vehicles:
        print(json.dumps(v.specs()))