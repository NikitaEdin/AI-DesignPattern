from abc import ABC, abstractmethod
import sys

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

class VehicleProducer:
    def create_vehicle(self, vehicle_type):
        if vehicle_type == "car":
            return Car()
        elif vehicle_type == "motorcycle":
            return Motorcycle()
        else:
            raise ValueError(f"Unknown vehicle type: {vehicle_type}")

def main():
    producer = VehicleProducer()
    
    try:
        car = producer.create_vehicle("car")
        print(car.start_engine())
        
        bike = producer.create_vehicle("motorcycle")
        print(bike.start_engine())
        
        invalid = producer.create_vehicle("truck")
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()