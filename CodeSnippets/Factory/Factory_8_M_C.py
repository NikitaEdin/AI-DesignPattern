from abc import ABC, abstractmethod
from typing import Dict, Type

class Vehicle(ABC):
    def __init__(self, model: str):
        self.model = model
    
    @abstractmethod
    def start_engine(self) -> str:
        pass
    
    @abstractmethod
    def get_specs(self) -> str:
        pass

class Car(Vehicle):
    def start_engine(self) -> str:
        return f"{self.model} car engine started with ignition"
    
    def get_specs(self) -> str:
        return f"{self.model}: 4 wheels, gasoline engine"

class Motorcycle(Vehicle):
    def start_engine(self) -> str:
        return f"{self.model} motorcycle engine started with kick/button"
    
    def get_specs(self) -> str:
        return f"{self.model}: 2 wheels, high performance engine"

class Truck(Vehicle):
    def start_engine(self) -> str:
        return f"{self.model} truck engine started with heavy-duty ignition"
    
    def get_specs(self) -> str:
        return f"{self.model}: 6+ wheels, diesel engine, cargo capacity"

class VehicleCreator:
    _vehicle_types: Dict[str, Type[Vehicle]] = {
        'car': Car,
        'motorcycle': Motorcycle,
        'truck': Truck
    }
    
    @classmethod
    def create_vehicle(cls, vehicle_type: str, model: str) -> Vehicle:
        if vehicle_type.lower() not in cls._vehicle_types:
            raise ValueError(f"Unknown vehicle type: {vehicle_type}")
        
        vehicle_class = cls._vehicle_types[vehicle_type.lower()]
        return vehicle_class(model)

if __name__ == "__main__":
    creator = VehicleCreator()
    
    vehicles = [
        creator.create_vehicle("car", "Tesla Model 3"),
        creator.create_vehicle("motorcycle", "Harley Davidson"),
        creator.create_vehicle("truck", "Ford F-150")
    ]
    
    for vehicle in vehicles:
        print(vehicle.get_specs())
        print(vehicle.start_engine())
        print("-" * 40)