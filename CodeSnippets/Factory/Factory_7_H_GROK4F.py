from abc import ABC, abstractmethod
from typing import Dict, Type, Any

class BaseVehicle(ABC):
    def __init__(self, color: str):
        self.color = color

    @abstractmethod
    def operate(self) -> str:
        pass

class Car(BaseVehicle):
    def operate(self) -> str:
        return f"The {self.color} car is driving on the road."

class Bike(BaseVehicle):
    def operate(self) -> str:
        return f"The {self.color} bike is pedaling along the path."

class BaseMaker(ABC):
    @abstractmethod
    def make_vehicle(self, color: str) -> BaseVehicle:
        pass

class CarMaker(BaseMaker):
    def make_vehicle(self, color: str) -> BaseVehicle:
        return Car(color)

class BikeMaker(BaseMaker):
    def make_vehicle(self, color: str) -> BaseVehicle:
        return Bike(color)

class VehicleWorkshop:
    def __init__(self):
        self._makers: Dict[str, Type[BaseMaker]] = {
            'car': CarMaker,
            'bike': BikeMaker
        }

    def create_vehicle(self, vehicle_type: str, color: str) -> BaseVehicle:
        if vehicle_type not in self._makers:
            raise ValueError(f"Unsupported vehicle type: {vehicle_type}")
        maker: BaseMaker = self._makers[vehicle_type]()
        return maker.make_vehicle(color)

if __name__ == "__main__":
    workshop = VehicleWorkshop()
    car = workshop.create_vehicle('car', 'red')
    print(car.operate())
    bike = workshop.create_vehicle('bike', 'blue')
    print(bike.operate())
    try:
        invalid = workshop.create_vehicle('truck', 'green')
    except ValueError as e:
        print(f"Error: {e}")