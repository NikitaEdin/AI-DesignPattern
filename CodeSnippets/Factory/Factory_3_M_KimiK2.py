from abc import ABC, abstractmethod

class Vehicle(ABC):
    @abstractmethod
    def drive(self):
        pass

class Car(Vehicle):
    def drive(self):
        return "Driving a car"

class Motorcycle(Vehicle):
    def drive(self):
        return "Riding a motorcycle"

class VehicleProvider:
    _vehicles = {"car": Car, "motorcycle": Motorcycle}
    
    @classmethod
    def create(cls, vehicle_type):
        if vehicle_type not in cls._vehicles:
            raise ValueError(f"Unknown vehicle type: {vehicle_type}")
        return cls._vehicles[vehicle_type]()

if __name__ == "__main__":
    for vtype in ["car", "motorcycle"]:
        vehicle = VehicleProvider.create(vtype)
        print(vehicle.drive())