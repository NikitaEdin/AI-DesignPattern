from abc import ABC, abstractmethod

class Vehicle(ABC):
    @abstractmethod
    def start(self):
        pass
    
    @abstractmethod
    def get_info(self):
        pass

class Car(Vehicle):
    def __init__(self, model="Sedan"):
        self.model = model
        self.wheels = 4
    
    def start(self):
        return f"{self.model} car engine started"
    
    def get_info(self):
        return f"Car: {self.model}, Wheels: {self.wheels}"

class Motorcycle(Vehicle):
    def __init__(self, model="Sport"):
        self.model = model
        self.wheels = 2
    
    def start(self):
        return f"{self.model} motorcycle engine revved"
    
    def get_info(self):
        return f"Motorcycle: {self.model}, Wheels: {self.wheels}"

class Truck(Vehicle):
    def __init__(self, model="Heavy Duty"):
        self.model = model
        self.wheels = 6
    
    def start(self):
        return f"{self.model} truck engine rumbled"
    
    def get_info(self):
        return f"Truck: {self.model}, Wheels: {self.wheels}"

class VehicleCreator:
    @staticmethod
    def create_vehicle(vehicle_type, model=None):
        vehicle_types = {
            "car": Car,
            "motorcycle": Motorcycle,
            "truck": Truck
        }
        
        if vehicle_type.lower() not in vehicle_types:
            raise ValueError(f"Unknown vehicle type: {vehicle_type}")
        
        vehicle_class = vehicle_types[vehicle_type.lower()]
        return vehicle_class(model) if model else vehicle_class()

if __name__ == "__main__":
    creator = VehicleCreator()
    
    vehicles = [
        creator.create_vehicle("car", "Luxury Sedan"),
        creator.create_vehicle("motorcycle"),
        creator.create_vehicle("truck", "Construction")
    ]
    
    for vehicle in vehicles:
        print(vehicle.get_info())
        print(vehicle.start())
        print()