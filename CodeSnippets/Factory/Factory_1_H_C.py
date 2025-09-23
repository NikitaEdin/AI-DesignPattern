from abc import ABC, abstractmethod
from typing import Dict, Type, Any, Optional
from enum import Enum
import json

class VehicleType(Enum):
    CAR = "car"
    MOTORCYCLE = "motorcycle"
    TRUCK = "truck"

class Vehicle(ABC):
    def __init__(self, model: str, year: int):
        self.model = model
        self.year = year
        self.features = {}
    
    @abstractmethod
    def get_info(self) -> str:
        pass
    
    @abstractmethod
    def get_base_price(self) -> float:
        pass
    
    def add_feature(self, feature: str, value: Any):
        self.features[feature] = value

class Car(Vehicle):
    def __init__(self, model: str, year: int, doors: int = 4):
        super().__init__(model, year)
        self.doors = doors
    
    def get_info(self) -> str:
        return f"{self.year} {self.model} Car ({self.doors} doors)"
    
    def get_base_price(self) -> float:
        return 25000.0

class Motorcycle(Vehicle):
    def __init__(self, model: str, year: int, engine_cc: int = 500):
        super().__init__(model, year)
        self.engine_cc = engine_cc
    
    def get_info(self) -> str:
        return f"{self.year} {self.model} Motorcycle ({self.engine_cc}cc)"
    
    def get_base_price(self) -> float:
        return 15000.0

class Truck(Vehicle):
    def __init__(self, model: str, year: int, payload: int = 5000):
        super().__init__(model, year)
        self.payload = payload
    
    def get_info(self) -> str:
        return f"{self.year} {self.model} Truck ({self.payload}kg payload)"
    
    def get_base_price(self) -> float:
        return 45000.0

class VehicleCreator:
    _registry: Dict[VehicleType, Type[Vehicle]] = {}
    
    @classmethod
    def register(cls, vehicle_type: VehicleType, vehicle_class: Type[Vehicle]):
        cls._registry[vehicle_type] = vehicle_class
    
    @classmethod
    def create(cls, vehicle_type: VehicleType, **kwargs) -> Optional[Vehicle]:
        if vehicle_type not in cls._registry:
            raise ValueError(f"Unknown vehicle type: {vehicle_type}")
        
        vehicle_class = cls._registry[vehicle_type]
        return vehicle_class(**kwargs)
    
    @classmethod
    def create_from_config(cls, config: str) -> Vehicle:
        data = json.loads(config)
        vehicle_type = VehicleType(data.pop('type'))
        vehicle = cls.create(vehicle_type, **data)
        
        if 'features' in data:
            for feature, value in data['features'].items():
                vehicle.add_feature(feature, value)
        
        return vehicle
    
    @classmethod
    def get_available_types(cls) -> list:
        return list(cls._registry.keys())

VehicleCreator.register(VehicleType.CAR, Car)
VehicleCreator.register(VehicleType.MOTORCYCLE, Motorcycle)
VehicleCreator.register(VehicleType.TRUCK, Truck)

if __name__ == "__main__":
    car = VehicleCreator.create(VehicleType.CAR, model="Sedan", year=2023, doors=2)
    motorcycle = VehicleCreator.create(VehicleType.MOTORCYCLE, model="Sport", year=2023, engine_cc=1000)
    truck = VehicleCreator.create(VehicleType.TRUCK, model="Heavy", year=2023, payload=10000)
    
    vehicles = [car, motorcycle, truck]
    
    for vehicle in vehicles:
        vehicle.add_feature("color", "red")
        print(f"{vehicle.get_info()} - ${vehicle.get_base_price():,.2f}")
    
    config_json = '{"type": "car", "model": "Luxury", "year": 2024, "doors": 4, "features": {"sunroof": true, "leather": true}}'
    luxury_car = VehicleCreator.create_from_config(config_json)
    print(f"\nFrom config: {luxury_car.get_info()} - Features: {luxury_car.features}")
    
    print(f"\nAvailable types: {[t.value for t in VehicleCreator.get_available_types()]}")