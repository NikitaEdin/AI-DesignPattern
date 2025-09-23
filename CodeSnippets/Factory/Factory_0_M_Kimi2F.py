class Vehicle:
    def __init__(self, brand):
        self.brand = brand

    def start(self):
        raise NotImplementedError

class Car(Vehicle):
    def start(self):
        return f"{self.brand} car engine started"

class Motorcycle(Vehicle):
    def start(self):
        return f"{self.brand} motorcycle engine started"

class Bicycle(Vehicle):
    def start(self):
        return f"{self.brand} bicycle is ready to ride"

class VehicleProducer:
    _registry = {
        "car": Car,
        "motorcycle": Motorcycle,
        "bicycle": Bicycle
    }

    @classmethod
    def create(cls, vehicle_type, brand):
        if vehicle_type not in cls._registry:
            raise ValueError(f"Unknown type: {vehicle_type}")
        return cls._registry[vehicle_type](brand)

if __name__ == "__main__":
    try:
        my_car = VehicleProducer.create("car", "Toyota")
        my_bike = VehicleProducer.create("bicycle", "Trek")
        my_motorcycle = VehicleProducer.create("motorcycle", "Harley")

        print(my_car.start())
        print(my_bike.start())
        print(my_motorcycle.start())

        unknown = VehicleProducer.create("spaceship", "SpaceX")
    except ValueError as e:
        print(f"Error: {e}")