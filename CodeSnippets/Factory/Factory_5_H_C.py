from abc import ABC, abstractmethod
from typing import Dict, Any
import json

class Vehicle(ABC):
    def __init__(self, model: str, **kwargs):
        self.model = model
        self.__dict__.update(kwargs)
    
    @abstractmethod
    def get_specs(self) -> Dict[str, Any]:
        pass
    
    def __repr__(self):
        return f"{self.__class__.__name__}(model='{self.model}')"

class Car(Vehicle):
    def __init__(self, model: str, doors: int = 4, fuel_type: str = "gasoline"):
        super().__init__(model, doors=doors, fuel_type=fuel_type)
    
    def get_specs(self) -> Dict[str, Any]:
        return {"type": "car", "model": self.model, "doors": self.doors, "fuel_type": self.fuel_type}

class Motorcycle(Vehicle):
    def __init__(self, model: str, engine_cc: int = 250, has_sidecar: bool = False):
        super().__init__(model, engine_cc=engine_cc, has_sidecar=has_sidecar)
    
    def get_specs(self) -> Dict[str, Any]:
        return {"type": "motorcycle", "model": self.model, "engine_cc": self.engine_cc, "has_sidecar": self.has_sidecar}

class Truck(Vehicle):
    def __init__(self, model: str, payload_tons: float = 5.0, axles: int = 2):
        super().__init__(model, payload_tons=payload_tons, axles=axles)
    
    def get_specs(self) -> Dict[str, Any]:
        return {"type": "truck", "model": self.model, "payload_tons": self.payload_tons, "axles": self.axles}

class VehicleCreator(ABC):
    @abstractmethod
    def create_vehicle(self, model: str, **kwargs) -> Vehicle:
        pass
    
    def create_from_config(self, config: Dict[str, Any]) -> Vehicle:
        model = config.pop('model')
        return self.create_vehicle(model, **config)

class CarCreator(VehicleCreator):
    def create_vehicle(self, model: str, **kwargs) -> Vehicle:
        return Car(model, **kwargs)

class MotorcycleCreator(VehicleCreator):
    def create_vehicle(self, model: str, **kwargs) -> Vehicle:
        return Motorcycle(model, **kwargs)

class TruckCreator(VehicleCreator):
    def create_vehicle(self, model: str, **kwargs) -> Vehicle:
        return Truck(model, **kwargs)

class VehicleManager:
    def __init__(self):
        self._creators = {
            'car': CarCreator(),
            'motorcycle': MotorcycleCreator(),
            'truck': TruckCreator()
        }
    
    def get_creator(self, vehicle_type: str) -> VehicleCreator:
        if vehicle_type not in self._creators:
            raise ValueError(f"Unknown vehicle type: {vehicle_type}")
        return self._creators[vehicle_type]
    
    def create_vehicle(self, vehicle_type: str, model: str, **kwargs) -> Vehicle:
        creator = self.get_creator(vehicle_type)
        return creator.create_vehicle(model, **kwargs)
    
    def create_batch(self, configs: list) -> list:
        vehicles = []
        for config in configs:
            vehicle_type = config.pop('type')
            creator = self.get_creator(vehicle_type)
            vehicles.append(creator.create_from_config(config))
        return vehicles

if __name__ == "__main__":
    manager = VehicleManager()
    
    sedan = manager.create_vehicle('car', 'Camry', doors=4, fuel_type='hybrid')
    bike = manager.create_vehicle('motorcycle', 'Ninja', engine_cc=600)
    pickup = manager.create_vehicle('truck', 'F-150', payload_tons=1.5)
    
    print(f"Created: {sedan}")
    print(f"Specs: {sedan.get_specs()}")
    
    configs = [
        {'type': 'car', 'model': 'Model S', 'fuel_type': 'electric'},
        {'type': 'motorcycle', 'model': 'Harley', 'engine_cc': 1200, 'has_sidecar': True}
    ]
    
    batch_vehicles = manager.create_batch(configs)
    for vehicle in batch_vehicles:
        print(f"Batch created: {vehicle} - {vehicle.get_specs()}")