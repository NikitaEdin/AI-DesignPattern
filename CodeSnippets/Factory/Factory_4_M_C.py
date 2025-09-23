from abc import ABC, abstractmethod
from enum import Enum

class VehicleType(Enum):
    CAR = "car"
    MOTORCYCLE = "motorcycle"
    TRUCK = "truck"

class Vehicle(ABC):
    def __init__(self, brand, model):
        self.brand = brand
        self.model = model
    
    @abstractmethod
    def start_engine(self):
        pass
    
    @abstractmethod
    def get_specs(self):
        pass

class Car(Vehicle):
    def start_engine(self):
        return f"{self.brand} {self.model} car engine started with key"
    
    def get_specs(self):
        return f"4-wheel {self.brand} {self.model} with 4 doors"

class Motorcycle(Vehicle):
    def start_engine(self):
        return f"{self.brand} {self.model} motorcycle engine started with button"
    
    def get_specs(self):
        return f"2-wheel {self.brand} {self.model} with handlebars"

class Truck(Vehicle):
    def start_engine(self):
        return f"{self.brand} {self.model} truck engine started with air system"
    
    def get_specs(self):
        return f"Heavy-duty {self.brand} {self.model} with cargo bed"

class VehicleCreator:
    @staticmethod
    def create_vehicle(vehicle_type, brand, model):
        if not isinstance(vehicle_type, VehicleType):
            raise ValueError("Invalid vehicle type provided")
        
        if vehicle_type == VehicleType.CAR:
            return Car(brand, model)
        elif vehicle_type == VehicleType.MOTORCYCLE:
            return Motorcycle(brand, model)
        elif vehicle_type == VehicleType.TRUCK:
            return Truck(brand, model)

if __name__ == "__main__":
    creator = VehicleCreator()
    
    vehicles = [
        creator.create_vehicle(VehicleType.CAR, "Toyota", "Camry"),
        creator.create_vehicle(VehicleType.MOTORCYCLE, "Honda", "CBR"),
        creator.create_vehicle(VehicleType.TRUCK, "Ford", "F-150")
    ]
    
    for vehicle in vehicles:
        print(vehicle.get_specs())
        print(vehicle.start_engine())
        print()