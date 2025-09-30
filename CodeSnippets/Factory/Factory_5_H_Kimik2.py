from abc import ABC, abstractmethod
import random
import threading
from typing import Dict, Type

class Vehicle(ABC):
    def __init__(self, identifier: str):
        self.identifier = identifier
        self.speed = 0
    
    @abstractmethod
    def accelerate(self) -> str:
        pass
    
    @abstractmethod
    def brake(self) -> str:
        pass
    
    def get_status(self) -> str:
        return f"{self.__class__.__name__} {self.identifier}: {self.speed} km/h"

class Car(Vehicle):
    def __init__(self, identifier: str):
        super().__init__(identifier)
        self.max_speed = 200
    
    def accelerate(self) -> str:
        self.speed = min(self.speed + 20, self.max_speed)
        return f"Car {self.identifier} accelerating to {self.speed} km/h"
    
    def brake(self) -> str:
        self.speed = max(self.speed - 30, 0)
        return f"Car {self.identifier} braking to {self.speed} km/h"

class Motorcycle(Vehicle):
    def __init__(self, identifier: str):
        super().__init__(identifier)
        self.max_speed = 180
    
    def accelerate(self) -> str:
        self.speed = min(self.speed + 30, self.max_speed)
        return f"Motorcycle {self.identifier} accelerating to {self.speed} km/h"
    
    def brake(self) -> str:
        self.speed = max(self.speed - 25, 0)
        return f"Motorcycle {self.identifier} braking to {self.speed} km/h"

class VehicleProducer:
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self._producers: Dict[str, Type[Vehicle]] = {
            'car': Car,
            'motorcycle': Motorcycle
        }
        self._created_vehicles = []
    
    def register_producer(self, vehicle_type: str, producer_class: Type[Vehicle]):
        self._producers[vehicle_type.lower()] = producer_class
    
    def create(self, vehicle_type: str, identifier: str = None) -> Vehicle:
        vehicle_type = vehicle_type.lower()
        if vehicle_type not in self._producers:
            raise ValueError(f"Unknown vehicle type: {vehicle_type}")
        
        if identifier is None:
            identifier = f"{vehicle_type.upper()}{random.randint(1000, 9999)}"
        
        producer_class = self._producers[vehicle_type]
        vehicle = producer_class(identifier)
        self._created_vehicles.append(vehicle)
        return vehicle
    
    def get_created_vehicles(self) -> list:
        return self._created_vehicles.copy()

if __name__ == "__main__":
    producer = VehicleProducer()
    
    car = producer.create("car", "C001")
    motorcycle = producer.create("motorcycle", "M001")
    
    print(car.accelerate())
    print(car.brake())
    print(motorcycle.accelerate())
    print(motorcycle.brake())
    
    print(f"\nCreated vehicles: {len(producer.get_created_vehicles())}")
    for vehicle in producer.get_created_vehicles():
        print(vehicle.get_status())