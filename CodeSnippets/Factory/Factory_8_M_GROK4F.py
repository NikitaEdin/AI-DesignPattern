from abc import ABC, abstractmethod

class Vehicle(ABC):
    @abstractmethod
    def start(self):
        pass

class Car(Vehicle):
    def start(self):
        return "Car engine starting"

class Motorcycle(Vehicle):
    def start(self):
        return "Motorcycle engine revving"

class VehicleSelector:
    _cache = {}

    @classmethod
    def select_vehicle(cls, vehicle_type):
        key = vehicle_type.lower().strip()
        if key not in cls._cache:
            if key == 'car':
                cls._cache[key] = Car()
            elif key == 'motorcycle':
                cls._cache[key] = Motorcycle()
            else:
                raise ValueError(f"Invalid vehicle type: {vehicle_type}")
        return cls._cache[key]

if __name__ == "__main__":
    try:
        v1 = VehicleSelector.select_vehicle("Car")
        print(v1.start())
        v2 = VehicleSelector.select_vehicle("car")
        print("Same instance:", v1 is v2)
        v3 = VehicleSelector.select_vehicle("Motorcycle")
        print(v3.start())
    except ValueError as e:
        print(e)