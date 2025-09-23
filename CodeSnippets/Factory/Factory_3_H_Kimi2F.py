from __future__ import annotations
from abc import ABC, abstractmethod
import json
import threading

class Vehicle(ABC):
    @abstractmethod
    def specs(self) -> dict: ...

class Car(Vehicle):
    def __init__(self, model: str):
        self.model = model
    def specs(self) -> dict:
        return {"type": "Car", "model": self.model, "wheels": 4}

class Bike(Vehicle):
    def __init__(self, model: str):
        self.model = model
    def specs(self) -> dict:
        return {"type": "Bike", "model": self.model, "wheels": 2}

class Creator(ABC):
    _lock = threading.Lock()
    _registry: dict[str, type[Creator]] = {}
    def __init_subclass__(cls, *, key: str, **kw):
        with cls._lock:
            cls._registry[key] = cls
        super().__init_subclass__(**kw)
    @abstractmethod
    def _produce(self, model: str) -> Vehicle: ...
    @classmethod
    def get_instance(cls, key: str) -> Creator:
        with cls._lock:
            if key not in cls._registry:
                raise ValueError(f"Unknown key: {key}")
            return cls._registry[key]()
    def deliver(self, model: str) -> Vehicle:
        return self._produce(model)

class CarBuilder(Creator, key="car"):
    def _produce(self, model: str) -> Vehicle:
        return Car(model)

class BikeBuilder(Creator, key="bike"):
    def _produce(self, model: str) -> Vehicle:
        return Bike(model)

if __name__ == "__main__":
    for k, m in [("car", "Tesla"), ("bike", "Yamaha")]:
        builder = Creator.get_instance(k)
        vehicle = builder.deliver(m)
        print(json.dumps(vehicle.specs()))