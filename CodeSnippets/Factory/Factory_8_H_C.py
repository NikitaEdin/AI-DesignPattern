from abc import ABC, abstractmethod
from enum import Enum
from typing import Dict, Type, Any
import json

class VehicleType(Enum):
    CAR = "car"
    TRUCK = "truck"
    MOTORCYCLE = "motorcycle"

class Vehicle(ABC):
    def __init__(self, config: Dict[str, Any]):
        self.brand = config.get('brand', 'Unknown')
        self.model = config.get('model', 'Unknown')
        self.year = config.get('year', 2023)
    
    @abstractmethod
    def start_engine(self) -> str:
        pass
    
    @abstractmethod
    def get_specs(self) -> Dict[str, Any]:
        pass

class Car(Vehicle):
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.doors = config.get('doors', 4)
        self.fuel_type = config.get('fuel_type', 'gasoline')
    
    def start_engine(self) -> str:
        return f"Car {self.brand} {self.model} engine started with {self.fuel_type}"
    
    def get_specs(self) -> Dict[str, Any]:
        return {
            'type': 'car',
            'brand': self.brand,
            'model': self.model,
            'year': self.year,
            'doors': self.doors,
            'fuel_type': self.fuel_type
        }

class Truck(Vehicle):
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.payload = config.get('payload', 1000)
        self.axles = config.get('axles', 2)
    
    def start_engine(self) -> str:
        return f"Truck {self.brand} {self.model} diesel engine started, payload: {self.payload}kg"
    
    def get_specs(self) -> Dict[str, Any]:
        return {
            'type': 'truck',
            'brand': self.brand,
            'model': self.model,
            'year': self.year,
            'payload': self.payload,
            'axles': self.axles
        }

class Motorcycle(Vehicle):
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.engine_cc = config.get('engine_cc', 250)
        self.bike_type = config.get('bike_type', 'sport')
    
    def start_engine(self) -> str:
        return f"Motorcycle {self.brand} {self.model} {self.engine_cc}cc engine started"
    
    def get_specs(self) -> Dict[str, Any]:
        return {
            'type': 'motorcycle',
            'brand': self.brand,
            'model': self.model,
            'year': self.year,
            'engine_cc': self.engine_cc,
            'bike_type': self.bike_type
        }

class VehicleBuilder:
    _registry: Dict[VehicleType, Type[Vehicle]] = {}
    
    @classmethod
    def register(cls, vehicle_type: VehicleType, vehicle_class: Type[Vehicle]):
        cls._registry[vehicle_type] = vehicle_class
    
    @classmethod
    def create(cls, vehicle_type: VehicleType, config: Dict[str, Any]) -> Vehicle:
        if vehicle_type not in cls._registry:
            raise ValueError(f"Unsupported vehicle type: {vehicle_type.value}")
        
        vehicle_class = cls._registry[vehicle_type]
        return vehicle_class(config)
    
    @classmethod
    def create_from_json(cls, json_config: str) -> Vehicle:
        config = json.loads(json_config)
        vehicle_type = VehicleType(config.pop('type'))
        return cls.create(vehicle_type, config)
    
    @classmethod
    def get_supported_types(cls) -> list:
        return [vtype.value for vtype in cls._registry.keys()]

VehicleBuilder.register(VehicleType.CAR, Car)
VehicleBuilder.register(VehicleType.TRUCK, Truck)
VehicleBuilder.register(VehicleType.MOTORCYCLE, Motorcycle)

if __name__ == "__main__":
    car_config = {'brand': 'Toyota', 'model': 'Camry', 'year': 2023, 'doors': 4, 'fuel_type': 'hybrid'}
    car = VehicleBuilder.create(VehicleType.CAR, car_config)
    
    truck_config = {'brand': 'Ford', 'model': 'F-150', 'payload': 1500, 'axles': 2}
    truck = VehicleBuilder.create(VehicleType.TRUCK, truck_config)
    
    json_config = '{"type": "motorcycle", "brand": "Yamaha", "model": "R6", "engine_cc": 600, "bike_type": "sport"}'
    motorcycle = VehicleBuilder.create_from_json(json_config)
    
    vehicles = [car, truck, motorcycle]
    
    for vehicle in vehicles:
        print(vehicle.start_engine())
        print(f"Specs: {vehicle.get_specs()}\n")
    
    print(f"Supported types: {VehicleBuilder.get_supported_types()}")