from abc import ABC, abstractmethod

class Vehicle(ABC):
    @abstractmethod
    def start(self):
        pass
    
    @abstractmethod
    def get_info(self):
        pass

class Car(Vehicle):
    def __init__(self, model):
        self.model = model
    
    def start(self):
        return f"Car {self.model} engine started"
    
    def get_info(self):
        return f"Car: {self.model}"

class Motorcycle(Vehicle):
    def __init__(self, model):
        self.model = model
    
    def start(self):
        return f"Motorcycle {self.model} engine revved"
    
    def get_info(self):
        return f"Motorcycle: {self.model}"

class Truck(Vehicle):
    def __init__(self, model):
        self.model = model
    
    def start(self):
        return f"Truck {self.model} diesel engine started"
    
    def get_info(self):
        return f"Truck: {self.model}"

class VehicleCreator:
    _registry = {
        'car': Car,
        'motorcycle': Motorcycle,
        'truck': Truck
    }
    
    @classmethod
    def create_vehicle(cls, vehicle_type, model):
        if vehicle_type.lower() not in cls._registry:
            raise ValueError(f"Unknown vehicle type: {vehicle_type}")
        
        vehicle_class = cls._registry[vehicle_type.lower()]
        return vehicle_class(model)
    
    @classmethod
    def get_available_types(cls):
        return list(cls._registry.keys())

if __name__ == "__main__":
    creator = VehicleCreator()
    
    vehicles = [
        creator.create_vehicle('car', 'Toyota Camry'),
        creator.create_vehicle('motorcycle', 'Harley Davidson'),
        creator.create_vehicle('truck', 'Ford F-150')
    ]
    
    for vehicle in vehicles:
        print(vehicle.get_info())
        print(vehicle.start())
        print()
    
    print("Available types:", creator.get_available_types())