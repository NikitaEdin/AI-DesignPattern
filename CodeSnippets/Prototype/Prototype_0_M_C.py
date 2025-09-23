import copy
from abc import ABC, abstractmethod

class Cloneable(ABC):
    @abstractmethod
    def clone(self):
        pass

class Vehicle(Cloneable):
    def __init__(self, brand, model, year, color):
        self.brand = brand
        self.model = model
        self.year = year
        self.color = color
        self.features = []

    def add_feature(self, feature):
        self.features.append(feature)

    def clone(self):
        try:
            return copy.deepcopy(self)
        except Exception as e:
            raise RuntimeError(f"Failed to clone vehicle: {e}")

    def __str__(self):
        return f"{self.year} {self.brand} {self.model} ({self.color}) - Features: {', '.join(self.features)}"

class VehicleRegistry:
    def __init__(self):
        self._templates = {}

    def register_template(self, name, vehicle):
        self._templates[name] = vehicle

    def create_vehicle(self, template_name):
        template = self._templates.get(template_name)
        if not template:
            raise ValueError(f"Template '{template_name}' not found")
        return template.clone()

if __name__ == "__main__":
    registry = VehicleRegistry()
    
    base_sedan = Vehicle("Toyota", "Camry", 2023, "Silver")
    base_sedan.add_feature("Air Conditioning")
    base_sedan.add_feature("Bluetooth")
    registry.register_template("standard_sedan", base_sedan)
    
    car1 = registry.create_vehicle("standard_sedan")
    car1.color = "Blue"
    car1.add_feature("Sunroof")
    
    car2 = registry.create_vehicle("standard_sedan")
    car2.year = 2024
    car2.add_feature("Navigation")
    
    print(car1)
    print(car2)
    print(base_sedan)