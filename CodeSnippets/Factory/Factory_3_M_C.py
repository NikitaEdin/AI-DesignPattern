from abc import ABC, abstractmethod

class Vehicle(ABC):
    @abstractmethod
    def start(self):
        pass
    
    @abstractmethod
    def stop(self):
        pass

class Car(Vehicle):
    def start(self):
        return "Car engine started"
    
    def stop(self):
        return "Car engine stopped"

class Motorcycle(Vehicle):
    def start(self):
        return "Motorcycle engine started"
    
    def stop(self):
        return "Motorcycle engine stopped"

class Truck(Vehicle):
    def start(self):
        return "Truck engine started"
    
    def stop(self):
        return "Truck engine stopped"

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
    
    print("Available vehicles:", creator.get_available_types())
    
    vehicles = ['car', 'motorcycle', 'truck']
    
    for vehicle_type in vehicles:
        vehicle = creator.create_vehicle(vehicle_type)
        print(f"{vehicle_type.capitalize()}: {vehicle.start()}")
        print(f"{vehicle_type.capitalize()}: {vehicle.stop()}")
    
    try:
        invalid_vehicle = creator.create_vehicle('airplane')
    except ValueError as e:
        print(f"Error: {e}")