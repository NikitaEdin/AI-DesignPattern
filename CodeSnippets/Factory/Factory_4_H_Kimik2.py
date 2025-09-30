import abc
from typing import Dict, Type, Optional, Any
import threading


class Vehicle(abc.ABC):
    @abc.abstractmethod
    def start(self) -> str:
        pass
    
    @abc.abstractmethod
    def stop(self) -> str:
        pass


class Car(Vehicle):
    def __init__(self, color: str = "red") -> None:
        self.color = color
        self._speed = 0
    
    def start(self) -> str:
        self._speed = 60
        return f"{self.color} car started at {self._speed} km/h"
    
    def stop(self) -> str:
        self._speed = 0
        return f"{self.color} car stopped"


class Motorcycle(Vehicle):
    def __init__(self, color: str = "black") -> None:
        self.color = color
        self._speed = 0
    
    def start(self) -> str:
        self._speed = 80
        return f"{self.color} motorcycle started at {self._speed} km/h"
    
    def stop(self) -> str:
        self._speed = 0
        return f"{self.color} motorcycle stopped"


class Truck(Vehicle):
    def __init__(self, capacity: int = 1000) -> None:
        self.capacity = capacity
        self._load = 0
    
    def start(self) -> str:
        return f"Truck with {self.capacity}kg capacity started"
    
    def stop(self) -> str:
        return f"Truck stopped with {self._load}kg load"


class VehicleProducer:
    _vehicles: Dict[str, Type[Vehicle]] = {}
    _lock = threading.Lock()
    
    @classmethod
    def register(cls, name: str, vehicle_class: Type[Vehicle]) -> None:
        with cls._lock:
            cls._vehicles[name] = vehicle_class
    
    @classmethod
    def create(cls, name: str, **kwargs: Any) -> Optional[Vehicle]:
        with cls._lock:
            vehicle_class = cls._vehicles.get(name)
            if vehicle_class:
                return vehicle_class(**kwargs)
            return None
    
    @classmethod
    def list_available(cls) -> list:
        with cls._lock:
            return list(cls._vehicles.keys())


def main() -> None:
    VehicleProducer.register("car", Car)
    VehicleProducer.register("motorcycle", Motorcycle)
    VehicleProducer.register("truck", Truck)
    
    print("Available types:", VehicleProducer.list_available())
    
    car = VehicleProducer.create("car", color="blue")
    if car:
        print(car.start())
        print(car.stop())
    
    bike = VehicleProducer.create("motorcycle", color="green")
    if bike:
        print(bike.start())
        print(bike.stop())
    
    truck = VehicleProducer.create("truck", capacity=2000)
    if truck:
        print(truck.start())
        print(truck.stop())
    
    unknown = VehicleProducer.create("plane")
    print("Unknown type result:", unknown is None)


if __name__ == "__main__":
    main()