# Base class for all factories
class Factory:
    def create(self, name):
        raise NotImplementedError("create method must be implemented")

# Concrete factory for creating vehicles
class VehicleFactory(Factory):
    def create(self, name):
        if name == "car":
            return Car()
        elif name == "bike":
            return Bike()
        else:
            raise ValueError("Invalid vehicle type")

# Concrete factory for creating animals
class AnimalFactory(Factory):
    def create(self, name):
        if name == "dog":
            return Dog()
        elif name == "cat":
            return Cat()
        else:
            raise ValueError("Invalid animal type")

# Usage example
if __name__ == "__main__":
    vehicle_factory = VehicleFactory()
    car = vehicle_factory.create("car")
    print(car)

    animal_factory = AnimalFactory()
    dog = animal_factory.create("dog")
    print(dog)