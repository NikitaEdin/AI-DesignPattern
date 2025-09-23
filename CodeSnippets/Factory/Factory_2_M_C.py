from abc import ABC, abstractmethod

class Vehicle(ABC):
    @abstractmethod
    def start_engine(self):
        pass
    
    @abstractmethod
    def get_specs(self):
        pass

class Car(Vehicle):
    def __init__(self, model):
        self.model = model
        self.engine_type = "V6"
    
    def start_engine(self):
        return f"{self.model} car engine started"
    
    def get_specs(self):
        return f"Car: {self.model}, Engine: {self.engine_type}"

class Motorcycle(Vehicle):
    def __init__(self, model):
        self.model = model
        self.engine_type = "Single Cylinder"
    
    def start_engine(self):
        return f"{self.model} motorcycle engine started"
    
    def get_specs(self):
        return f"Motorcycle: {self.model}, Engine: {self.engine_type}"

class Truck(Vehicle):
    def __init__(self, model):
        self.model = model
        self.engine_type = "V8 Diesel"
    
    def start_engine(self):
        return f"{self.model} truck engine started"
    
    def get_specs(self):
        return f"Truck: {self.model}, Engine: {self.engine_type}"

class VehicleCreator:
    @staticmethod
    def create_vehicle(vehicle_type, model):
        vehicle_types = {
            'car': Car,
            'motorcycle': Motorcycle,
            'truck': Truck
        }
        
        if vehicle_type.lower() not in vehicle_types:
            raise ValueError(f"Unknown vehicle type: {vehicle_type}")
        
        return vehicle_types[vehicle_type.lower()](model)

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
        print()