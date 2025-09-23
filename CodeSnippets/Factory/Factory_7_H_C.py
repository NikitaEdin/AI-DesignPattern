from abc import ABC, abstractmethod
from typing import Dict, Type, Any, Optional
import json

class Vehicle(ABC):
    def __init__(self, model: str, year: int):
        self.model = model
        self.year = year
    
    @abstractmethod
    def start_engine(self) -> str:
        pass
    
    @abstractmethod
    def get_specs(self) -> Dict[str, Any]:
        pass

class Car(Vehicle):
    def __init__(self, model: str, year: int, doors: int = 4):
        super().__init__(model, year)
        self.doors = doors
    
    def start_engine(self) -> str:
        return f"{self.model} car engine started with smooth acceleration"
    
    def get_specs(self) -> Dict[str, Any]:
        return {"type": "car", "model": self.model, "year": self.year, "doors": self.doors}

class Motorcycle(Vehicle):
    def __init__(self, model: str, year: int, engine_cc: int = 600):
        super().__init__(model, year)
        self.engine_cc = engine_cc
    
    def start_engine(self) -> str:
        return f"{self.model} motorcycle roars to life"
    
    def get_specs(self) -> Dict[str, Any]:
        return {"type": "motorcycle", "model": self.model, "year": self.year, "engine_cc": self.engine_cc}

class Truck(Vehicle):
    def __init__(self, model: str, year: int, payload: int = 2000):
        super().__init__(model, year)
        self.payload = payload
    
    def start_engine(self) -> str:
        return f"{self.model} truck engine rumbles powerfully"
    
    def get_specs(self) -> Dict[str, Any]:
        return {"type": "truck", "model": self.model, "year": self.year, "payload": self.payload}

class VehicleCreator:
    _registry: Dict[str, Type[Vehicle]] = {}
    _configurations: Dict[str, Dict[str, Any]] = {}
    
    @classmethod
    def register(cls, vehicle_type: str, vehicle_class: Type[Vehicle], 
                default_config: Optional[Dict[str, Any]] = None) -> None:
        cls._registry[vehicle_type.lower()] = vehicle_class
        if default_config:
            cls._configurations[vehicle_type.lower()] = default_config
    
    @classmethod
    def create(cls, vehicle_type: str, model: str, year: int, **kwargs) -> Vehicle:
        vehicle_type = vehicle_type.lower()
        if vehicle_type not in cls._registry:
            raise ValueError(f"Unknown vehicle type: {vehicle_type}")
        
        vehicle_class = cls._registry[vehicle_type]
        config = cls._configurations.get(vehicle_type, {})
        final_kwargs = {**config, **kwargs}
        
        try:
            return vehicle_class(model, year, **final_kwargs)
        except TypeError as e:
            raise ValueError(f"Invalid parameters for {vehicle_type}: {e}")
    
    @classmethod
    def create_from_config(cls, config_data: str) -> Vehicle:
        try:
            config = json.loads(config_data)
            vehicle_type = config.pop('type')
            return cls.create(vehicle_type, **config)
        except (json.JSONDecodeError, KeyError) as e:
            raise ValueError(f"Invalid configuration: {e}")
    
    @classmethod
    def get_registered_types(cls) -> list:
        return list(cls._registry.keys())

if __name__ == "__main__":
    VehicleCreator.register("car", Car, {"doors": 4})
    VehicleCreator.register("motorcycle", Motorcycle, {"engine_cc": 750})
    VehicleCreator.register("truck", Truck, {"payload": 3000})
    
    vehicles = [
        VehicleCreator.create("car", "Tesla Model 3", 2023, doors=2),
        VehicleCreator.create("motorcycle", "Harley Davidson", 2022),
        VehicleCreator.create("truck", "Ford F-150", 2023, payload=2500)
    ]
    
    for vehicle in vehicles:
        print(vehicle.start_engine())
        print(f"Specs: {vehicle.get_specs()}")
    
    config_json = '{"type": "car", "model": "BMW X5", "year": 2023, "doors": 5}'
    config_vehicle = VehicleCreator.create_from_config(config_json)
    print(f"\nFrom config: {config_vehicle.get_specs()}")
    
    print(f"\nRegistered types: {VehicleCreator.get_registered_types()}")