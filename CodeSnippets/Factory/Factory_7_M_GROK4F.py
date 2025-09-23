from abc import ABC, abstractmethod

class Vehicle(ABC):
    @abstractmethod
    def start_engine(self):
        pass

class Car(Vehicle):
    def start_engine(self):
        return "Car engine started with a roar."

class Motorcycle(Vehicle):
    def start_engine(self):
        return "Motorcycle engine revved up."

class VehicleWorkshop:
    @classmethod
    def create_vehicle(cls, vehicle_type):
        if vehicle_type.lower() == "car":
            return Car()
        elif vehicle_type.lower() == "motorcycle":
            return Motorcycle()
        else:
            raise ValueError(f"Unsupported vehicle type: {vehicle_type}")

if __name__ == "__main__":
    try:
        car = VehicleWorkshop.create_vehicle("car")
        print(car.start_engine())
        
        motorcycle = VehicleWorkshop.create_vehicle("motorcycle")
        print(motorcycle.start_engine())
        
        VehicleWorkshop.create_vehicle("truck")  # This should raise ValueError
    except ValueError as e:
        print(f"Error: {e}")