import abc
from typing import Dict, Type, Optional, Any

class Vehicle(abc.ABC):
    @abc.abstractmethod
    def start(self) -> str: ...
    @abc.abstractmethod
    def specs(self) -> Dict[str, Any]: ...

class Car(Vehicle):
    def __init__(self, model: str, fuel: str = "gasoline"):
        self.model = model
        self.fuel = fuel
    def start(self) -> str:
        return f"{self.model} car ignites {self.fuel}"
    def specs(self) -> Dict[str, Any]:
        return {"wheels": 4, "fuel": self.fuel}

class Bike(Vehicle):
    def __init__(self, model: str, type_: str = "sport"):
        self.model = model
        self.type_ = type_
    def start(self) -> str:
        return f"{self.model} bike kicks {self.type_}"
    def specs(self) -> Dict[str, Any]:
        return {"wheels": 2, "type": self.type_}

class Truck(Vehicle):
    def __init__(self, model: str, capacity: int = 1000):
        self.model = model
        self.capacity = capacity
    def start(self) -> str:
        return f"{self.model} truck rumbles {self.capacity}kg"
    def specs(self) -> Dict[str, Any]:
        return {"wheels": 6, "capacity": self.capacity}

class Creator:
    _registry: Dict[str, Type[Vehicle]] = {}
    @classmethod
    def register(cls, key: str, vehicle_cls: Type[Vehicle]) -> None:
        cls._registry[key] = vehicle_cls
    @classmethod
    def build(cls, key: str, **kwargs) -> Vehicle:
        if key not in cls._registry:
            raise ValueError(f"Unknown key '{key}'")
        return cls._registry[key](**kwargs)
    @classmethod
    def list_types(cls) -> list:
        return list(cls._registry.keys())

Creator.register("car", Car)
Creator.register("bike", Bike)
Creator.register("truck", Truck)

if __name__ == "__main__":
    vehicles = [
        Creator.build("car", model="Tesla", fuel="electric"),
        Creator.build("bike", model="Yamaha", type_="racing"),
        Creator.build("truck", model="Ford", capacity=1500)
    ]
    for v in vehicles:
        print(v.start(), v.specs())