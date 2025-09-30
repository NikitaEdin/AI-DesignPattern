import abc
from typing import Dict, Type, Optional

class Vehicle(abc.ABC):
    @abc.abstractmethod
    def start(self) -> str:
        pass

    @abc.abstractmethod
    def specs(self) -> Dict[str, str]:
        pass

class Car(Vehicle):
    def __init__(self, model: str) -> None:
        self.model = model

    def start(self) -> str:
        return f"{self.model} car engine ignited"

    def specs(self) -> Dict[str, str]:
        return {"wheels": "4", "fuel": "gasoline"}

class Motorcycle(Vehicle):
    def __init__(self, model: str) -> None:
        self.model = model

    def start(self) -> str:
        return f"{self.model} motorcycle engine started"

    def specs(self) -> Dict[str, str]:
        return {"wheels": "2", "fuel": "gasoline"}

class ElectricScooter(Vehicle):
    def __init__(self, model: str) -> None:
        self.model = model

    def start(self) -> str:
        return f"{self.model} electric scooter powered on"

    def specs(self) -> Dict[str, str]:
        return {"wheels": "2", "fuel": "electric"}

class VehicleProducer:
    _registry: Dict[str, Type[Vehicle]] = {}
    _fallback: Optional[Type[Vehicle]] = None

    @classmethod
    def register(cls, key: str, vehicle_cls: Type[Vehicle]) -> None:
        cls._registry[key.lower()] = vehicle_cls

    @classmethod
    def set_fallback(cls, vehicle_cls: Type[Vehicle]) -> None:
        cls._fallback = vehicle_cls

    @classmethod
    def create(cls, key: str, model: str) -> Vehicle:
        vehicle_cls = cls._registry.get(key.lower(), cls._fallback)
        if vehicle_cls is None:
            raise ValueError(f"Unknown vehicle type: {key}")
        return vehicle_cls(model)

VehicleProducer.register("car", Car)
VehicleProducer.register("motorcycle", Motorcycle)
VehicleProducer.register("scooter", ElectricScooter)
VehicleProducer.set_fallback(Car)

if __name__ == "__main__":
    vehicles = [
        VehicleProducer.create("car", "Tesla Model 3"),
        VehicleProducer.create("motorcycle", "Harley Davidson"),
        VehicleProducer.create("scooter", "Xiaomi Mi"),
        VehicleProducer.create("unknown", "Generic Model")
    ]
    for v in vehicles:
        print(v.start())
        print(v.specs())