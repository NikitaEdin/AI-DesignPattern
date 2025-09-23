from abc import ABC, abstractmethod
from enum import Enum
from typing import Dict, Type, Any
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
    def start_engine(self) -> str:
        pass
    
    @abstractmethod
    def get_max_speed(self) -> int:
        pass
    
    def add_feature(self, name: str, value: Any):
        self.features[name] = value
    
    def serialize(self) -> str:
        return json.dumps({
            'type': self.__class__.__name__.lower(),
            'model': self.model,
            'year': self.year,
            'features': self.features
        })

class Car(Vehicle):
    def __init__(self, model: str, year: int, doors: int = 4):
        super().__init__(model, year)
        self.doors = doors
    
    def start_engine(self) -> str:
        return f"{self.model} car engine started"
    
    def get_max_speed(self) -> int:
        return 180

class Motorcycle(Vehicle):
    def __init__(self, model: str, year: int, engine_size: int = 600):
        super().__init__(model, year)
        self.engine_size = engine_size
    
    def start_engine(self) -> str:
        return f"{self.model} motorcycle engine roars"
    
    def get_max_speed(self) -> int:
        return 250

class Truck(Vehicle):
    def __init__(self, model: str, year: int, payload: int = 5000):
        super().__init__(model, year)
        self.payload = payload
    
    def start_engine(self) -> str:
        return f"{self.model} truck engine rumbles"
    
    def get_max_speed(self) -> int:
        return 120

class VehicleCreator:
    _registry: Dict[VehicleType, Type[Vehicle]] = {
        VehicleType.CAR: Car,
        VehicleType.MOTORCYCLE: Motorcycle,
        VehicleType.TRUCK: Truck
    }
    
    @classmethod
    def register_vehicle(cls, vehicle_type: VehicleType, vehicle_class: Type[Vehicle]):
        if not issubclass(vehicle_class, Vehicle):
            raise TypeError("Vehicle class must inherit from Vehicle")
        cls._registry[vehicle_type] = vehicle_class
    
    @classmethod
    def create(cls, vehicle_type: VehicleType, **kwargs) -> Vehicle:
        if vehicle_type not in cls._registry:
            raise ValueError(f"Unknown vehicle type: {vehicle_type}")
        
        vehicle_class = cls._registry[vehicle_type]
        
        try:
            return vehicle_class(**kwargs)
        except TypeError as e:
            raise ValueError(f"Invalid parameters for {vehicle_type.value}: {e}")
    
    @classmethod
    def create_from_config(cls, config: Dict[str, Any]) -> Vehicle:
        vehicle_type = VehicleType(config.pop('type'))
        vehicle = cls.create(vehicle_type, **config)
        
        if 'features' in config:
            for name, value in config['features'].items():
                vehicle.add_feature(name, value)
        
        return vehicle

if __name__ == "__main__":
    creator = VehicleCreator()
    
    car = creator.create(VehicleType.CAR, model="Tesla Model 3", year=2023, doors=4)
    motorcycle = creator.create(VehicleType.MOTORCYCLE, model="Yamaha R1", year=2023, engine_size=1000)
    truck = creator.create(VehicleType.TRUCK, model="Ford F-150", year=2023, payload=6000)
    
    vehicles = [car, motorcycle, truck]
    
    for vehicle in vehicles:
        print(f"{vehicle.start_engine()} - Max Speed: {vehicle.get_max_speed()} km/h")
    
    config = {
        'type': 'car',
        'model': 'BMW X5',
        'year': 2024,
        'doors': 5,
        'features': {'autopilot': True, 'sunroof': True}
    }
    
    custom_car = creator.create_from_config(config)
    print(f"\nCustom vehicle: {custom_car.serialize()}")