from abc import ABC, abstractmethod

class Vehicle(ABC):
    @abstractmethod
    def start_engine(self):
        pass
    
    @abstractmethod
    def get_specs(self):
        pass

class Car(Vehicle):
    def start_engine(self):
        return "Car engine started with key"
    
    def get_specs(self):
        return "4 wheels, seats 5, gasoline engine"

class Motorcycle(Vehicle):
    def start_engine(self):
        return "Motorcycle engine started with kick"
    
    def get_specs(self):
        return "2 wheels, seats 2, gasoline engine"

class Truck(Vehicle):
    def start_engine(self):
        return "Truck engine started with key"
    
    def get_specs(self):
        return "6+ wheels, cargo capacity, diesel engine"

class VehicleCreator:
    _vehicle_types = {
        'car': Car,
        'motorcycle': Motorcycle,
        'truck': Truck
    }
    
    @classmethod
    def create_vehicle(cls, vehicle_type):
        vehicle_type = vehicle_type.lower()
        if vehicle_type not in cls._vehicle_types:
            raise ValueError(f"Unknown vehicle type: {vehicle_type}")
        return cls._vehicle_types[vehicle_type]()
    
    @classmethod
    def get_available_types(cls):
        return list(cls._vehicle_types.keys())

if __name__ == "__main__":
    creator = VehicleCreator()
    
    for vehicle_type in creator.get_available_types():
        vehicle = creator.create_vehicle(vehicle_type)
        print(f"{vehicle_type.title()}: {vehicle.start_engine()}")
        print(f"Specs: {vehicle.get_specs()}\n")
    
    try:
        invalid_vehicle = creator.create_vehicle("airplane")
    except ValueError as e:
        print(f"Error: {e}")