from abc import ABC, abstractmethod
from typing import Dict, Type, Any
import json

class Vehicle(ABC):
    def __init__(self, model: str, year: int):
        self.model = model
        self.year = year
        self.features = []
    
    @abstractmethod
    def get_type(self) -> str:
        pass
    
    @abstractmethod
    def get_base_price(self) -> float:
        pass
    
    def add_feature(self, feature: str, cost: float = 0):
        self.features.append((feature, cost))
    
    def get_total_price(self) -> float:
        base = self.get_base_price()
        extras = sum(cost for _, cost in self.features)
        return base + extras
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'type': self.get_type(),
            'model': self.model,
            'year': self.year,
            'features': self.features,
            'total_price': self.get_total_price()
        }

class Car(Vehicle):
    def get_type(self) -> str:
        return "car"
    
    def get_base_price(self) -> float:
        return 25000.0

class Motorcycle(Vehicle):
    def get_type(self) -> str:
        return "motorcycle"
    
    def get_base_price(self) -> float:
        return 12000.0

class Truck(Vehicle):
    def get_type(self) -> str:
        return "truck"
    
    def get_base_price(self) -> float:
        return 45000.0

class VehicleCreator:
    _registry: Dict[str, Type[Vehicle]] = {}
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    @classmethod
    def register(cls, vehicle_type: str, vehicle_class: Type[Vehicle]):
        if not issubclass(vehicle_class, Vehicle):
            raise TypeError(f"{vehicle_class} must be a subclass of Vehicle")
        cls._registry[vehicle_type.lower()] = vehicle_class
    
    def create_vehicle(self, vehicle_type: str, model: str, year: int, 
                      features: Dict[str, float] = None) -> Vehicle:
        vehicle_type = vehicle_type.lower()
        if vehicle_type not in self._registry:
            available = ', '.join(self._registry.keys())
            raise ValueError(f"Unknown vehicle type: {vehicle_type}. Available: {available}")
        
        vehicle_class = self._registry[vehicle_type]
        vehicle = vehicle_class(model, year)
        
        if features:
            for feature_name, cost in features.items():
                vehicle.add_feature(feature_name, cost)
        
        return vehicle
    
    def get_supported_types(self) -> list:
        return list(self._registry.keys())

VehicleCreator.register("car", Car)
VehicleCreator.register("motorcycle", Motorcycle)
VehicleCreator.register("truck", Truck)

if __name__ == "__main__":
    creator = VehicleCreator()
    
    vehicles = [
        creator.create_vehicle("car", "Tesla Model 3", 2023, 
                             {"autopilot": 8000, "premium_sound": 2500}),
        creator.create_vehicle("motorcycle", "Harley Davidson", 2022, 
                             {"custom_paint": 1500}),
        creator.create_vehicle("truck", "Ford F-150", 2023)
    ]
    
    for vehicle in vehicles:
        print(json.dumps(vehicle.to_dict(), indent=2))
    
    try:
        creator.create_vehicle("submarine", "Yellow", 2023)
    except ValueError as e:
        print(f"Error: {e}")
    
    print(f"Supported types: {creator.get_supported_types()}")