from abc import ABC, abstractmethod
import json
from typing import Dict, Type

class Transport(ABC):
    @abstractmethod
    def move(self) -> str: ...
    
    @abstractmethod
    def capacity(self) -> int: ...

class Car(Transport):
    def move(self) -> str:
        return "Driving on roads"
    def capacity(self) -> int:
        return 5

class Boat(Transport):
    def move(self) -> str:
        return "Sailing on water"
    def capacity(self) -> int:
        return 30

class Plane(Transport):
    def move(self) -> str:
        return "Flying in air"
    def capacity(self) -> int:
        return 200

class Registry:
    _builders: Dict[str, Type[Transport]] = {}
    
    @classmethod
    def register(cls, key: str, transport_class: Type[Transport]):
        if not issubclass(transport_class, Transport):
            raise TypeError("Must be Transport subclass")
        cls._builders[key] = transport_class
    
    @classmethod
    def create(cls, key: str, **config) -> Transport:
        builder = cls._builders.get(key)
        if not builder:
            raise ValueError(f"Unknown key: {key}")
        return builder(**config)

Registry.register("car", Car)
Registry.register("boat", Boat)
Registry.register("plane", Plane)

class ConfigLoader:
    @staticmethod
    def from_json(path: str) -> Dict:
        with open(path) as f:
            return json.load(f)

if __name__ == "__main__":
    transports = ["car", "boat", "plane"]
    for t in transports:
        instance = Registry.create(t)
        print(f"{t.capitalize()}: {instance.move()} | Capacity: {instance.capacity()}")
    
    try:
        Registry.create("train")
    except ValueError as e:
        print(f"Error: {e}")