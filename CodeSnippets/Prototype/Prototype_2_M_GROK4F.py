class Vehicle:
    def __init__(self, make, model):
        self.make = make
        self.model = model
        self.features = []

    def add_feature(self, feature):
        if isinstance(feature, str):
            self.features.append(feature)
        else:
            raise ValueError("Feature must be a string")

    def duplicate(self):
        raise NotImplementedError("Subclasses must implement duplicate")

class Car(Vehicle):
    def __init__(self, make, model, color):
        super().__init__(make, model)
        self.color = color

    def duplicate(self):
        new_car = Car(self.make, self.model, self.color)
        new_car.features = self.features[:]
        return new_car

class Truck(Vehicle):
    def __init__(self, make, model, capacity):
        super().__init__(make, model)
        self.capacity = capacity

    def duplicate(self):
        new_truck = Truck(self.make, self.model, self.capacity)
        new_truck.features = self.features[:]
        return new_truck

class VehicleRegistry:
    def __init__(self):
        self._prototypes = {}

    def register(self, name, vehicle):
        if not isinstance(vehicle, Vehicle):
            raise ValueError("Must register a Vehicle instance")
        self._prototypes[name] = vehicle

    def create_vehicle(self, name):
        prototype = self._prototypes.get(name)
        if prototype is None:
            raise ValueError(f"No vehicle prototype registered under '{name}'")
        return prototype.duplicate()

if __name__ == "__main__":
    registry = VehicleRegistry()
    original_car = Car("Toyota", "Camry", "Red")
    original_car.add_feature("Leather Seats")
    registry.register("sedan", original_car)

    original_truck = Truck("Ford", "F-150", 2000)
    original_truck.add_feature("Towing Package")
    registry.register("pickup", original_truck)

    cloned_car = registry.create_vehicle("sedan")
    cloned_car.color = "Blue"
    cloned_car.add_feature("Navigation System")

    cloned_truck = registry.create_vehicle("pickup")
    cloned_truck.capacity = 2500

    print(f"Cloned Car: {cloned_car.make} {cloned_car.model}, Color: {cloned_car.color}, Features: {cloned_car.features}")
    print(f"Cloned Truck: {cloned_truck.make} {cloned_truck.model}, Capacity: {cloned_truck.capacity}, Features: {cloned_truck.features}")