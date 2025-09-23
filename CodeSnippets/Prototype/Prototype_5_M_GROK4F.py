import copy
from abc import ABC, abstractmethod
from typing import List

class Vehicle(ABC):
    def __init__(self, make: str, model: str):
        self.make = make
        self.model = model
        self.components: List[str] = []

    @abstractmethod
    def replicate(self) -> 'Vehicle':
        pass

    def add_component(self, component: str) -> None:
        self.components.append(component)

    def display_info(self) -> None:
        print(f"{self.make} {self.model} with components: {self.components}")

class Car(Vehicle):
    def __init__(self, make: str, model: str, doors: int):
        super().__init__(make, model)
        self.doors = doors

    def replicate(self) -> 'Car':
        new_car = Car(self.make, self.model, self.doors)
        new_car.components = copy.deepcopy(self.components)
        return new_car

class Truck(Vehicle):
    def __init__(self, make: str, model: str, capacity: float):
        super().__init__(make, model)
        self.capacity = capacity

    def replicate(self) -> 'Truck':
        new_truck = Truck(self.make, self.model, self.capacity)
        new_truck.components = copy.deepcopy(self.components)
        return new_truck

if __name__ == "__main__":
    original_car = Car("Toyota", "Camry", 4)
    original_car.add_component("Engine")
    original_car.add_component("Wheels")
    print("Original:")
    original_car.display_info()

    cloned_car = original_car.replicate()
    cloned_car.doors = 2
    cloned_car.add_component("Spoiler")
    print("\nCloned and modified:")
    cloned_car.display_info()

    original_car.display_info()