import copy
from abc import ABC, abstractmethod

class Cloneable(ABC):
    @abstractmethod
    def clone(self):
        pass

class Vehicle(Cloneable):
    def __init__(self, make, model, year, features=None):
        self.make = make
        self.model = model
        self.year = year
        self.features = features or []
        self._id = id(self)
    
    def clone(self):
        try:
            cloned = copy.deepcopy(self)
            cloned._id = id(cloned)
            return cloned
        except Exception as e:
            raise RuntimeError(f"Failed to clone vehicle: {e}")
    
    def add_feature(self, feature):
        self.features.append(feature)
    
    def __str__(self):
        return f"{self.year} {self.make} {self.model} (ID: {self._id}) - Features: {self.features}"

class VehicleFactory:
    def __init__(self):
        self._templates = {}
    
    def register_template(self, name, vehicle):
        if not isinstance(vehicle, Cloneable):
            raise ValueError("Vehicle must implement Cloneable interface")
        self._templates[name] = vehicle
    
    def create_vehicle(self, template_name):
        if template_name not in self._templates:
            raise KeyError(f"Template '{template_name}' not found")
        return self._templates[template_name].clone()

if __name__ == "__main__":
    factory = VehicleFactory()
    
    sedan_template = Vehicle("Toyota", "Camry", 2023, ["Air Conditioning", "Bluetooth"])
    factory.register_template("luxury_sedan", sedan_template)
    
    car1 = factory.create_vehicle("luxury_sedan")
    car2 = factory.create_vehicle("luxury_sedan")
    
    car2.add_feature("Sunroof")
    
    print(car1)
    print(car2)
    print(f"Same object: {car1 is car2}")