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
        return f"{self.model} car engine started"
    
    def get_info(self):
        return f"Car model: {self.model}"

class Motorcycle(Vehicle):
    def __init__(self, model):
        self.model = model
    
    def start(self):
        return f"{self.model} motorcycle engine revved"
    
    def get_info(self):
        return f"Motorcycle model: {self.model}"

class Truck(Vehicle):
    def __init__(self, model):
        self.model = model
    
    def start(self):
        return f"{self.model} truck engine rumbled to life"
    
    def get_info(self):
        return f"Truck model: {self.model}"

class VehicleBuilder:
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
    builder = VehicleBuilder()
    
    vehicles = [
        builder.create_vehicle("car", "Toyota Camry"),
        builder.create_vehicle("motorcycle", "Harley Davidson"),
        builder.create_vehicle("truck", "Ford F-150")
    ]
    
    for vehicle in vehicles:
        print(vehicle.get_info())
        print(vehicle.start())
        print()