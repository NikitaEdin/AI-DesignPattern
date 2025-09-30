from abc import ABC, abstractmethod

class Vehicle(ABC):
    @abstractmethod
    def description(self):
        pass

class Car(Vehicle):
    def description(self):
        return "Sedan car"

class Motorcycle(Vehicle):
    def description(self):
        return "Sport motorcycle"

class VehicleProducer(ABC):
    @abstractmethod
    def build(self, vehicle_type):
        pass

class StandardVehicleProducer(VehicleProducer):
    def __init__(self):
        self.vehicle_registry = {
            'car': Car,
            'motorcycle': Motorcycle
        }
    
    def build(self, vehicle_type):
        if vehicle_type not in self.vehicle_registry:
            raise ValueError(f"Unknown vehicle type: {vehicle_type}")
        return self.vehicle_registry[vehicle_type]()
    
    def register_vehicle(self, vehicle_type, vehicle_class):
        self.vehicle_registry[vehicle_type] = vehicle_class

class LuxuryVehicleProducer(VehicleProducer):
    def __init__(self):
        self.vehicle_registry = {
            'car': lambda: type('LuxuryCar', (Car,), {'description': lambda s: "Luxury sedan with premium features"})()
        }
    
    def build(self, vehicle_type):
        if vehicle_type not in self.vehicle_registry:
            raise ValueError(f"Luxury producer cannot create: {vehicle_type}")
        return self.vehicle_registry[vehicle_type]()

if __name__ == "__main__":
    producer = StandardVehicleProducer()
    vehicle = producer.build('car')
    print(vehicle.description())
    
    producer = LuxuryVehicleProducer()
    vehicle = producer.build('car')
    print(vehicle.description())