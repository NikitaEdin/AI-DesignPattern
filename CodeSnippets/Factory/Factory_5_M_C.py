from abc import ABC, abstractmethod

class Vehicle(ABC):
    @abstractmethod
    def start_engine(self):
        pass
    
    @abstractmethod
    def get_fuel_type(self):
        pass

class Car(Vehicle):
    def start_engine(self):
        return "Car engine started with key"
    
    def get_fuel_type(self):
        return "gasoline"

class Motorcycle(Vehicle):
    def start_engine(self):
        return "Motorcycle engine started with button"
    
    def get_fuel_type(self):
        return "gasoline"

class Truck(Vehicle):
    def start_engine(self):
        return "Truck engine started with key"
    
    def get_fuel_type(self):
        return "diesel"

class VehicleCreator:
    _vehicle_types = {
        'car': Car,
        'motorcycle': Motorcycle,
        'truck': Truck
    }
    
    @classmethod
    def create_vehicle(cls, vehicle_type):
        if vehicle_type.lower() not in cls._vehicle_types:
            raise ValueError(f"Unknown vehicle type: {vehicle_type}")
        return cls._vehicle_types[vehicle_type.lower()]()
    
    @classmethod
    def get_available_types(cls):
        return list(cls._vehicle_types.keys())

if __name__ == "__main__":
    creator = VehicleCreator()
    
    try:
        car = creator.create_vehicle("car")
        print(car.start_engine())
        print(f"Fuel type: {car.get_fuel_type()}")
        
        bike = creator.create_vehicle("motorcycle")
        print(bike.start_engine())
        
        truck = creator.create_vehicle("truck")
        print(f"Truck fuel: {truck.get_fuel_type()}")
        
        print(f"Available types: {creator.get_available_types()}")
        
    except ValueError as e:
        print(f"Error: {e}")