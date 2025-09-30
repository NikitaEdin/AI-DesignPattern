class Vehicle:
    def start_engine(self):
        raise NotImplementedError

class Car(Vehicle):
    def start_engine(self):
        return "Car engine started"

class Motorcycle(Vehicle):
    def start_engine(self):
        return "Motorcycle engine started"

class VehicleProducer:
    _registry = {}

    @classmethod
    def register(cls, name, subclass):
        cls._registry[name] = subclass

    @classmethod
    def create(cls, name):
        if name not in cls._registry:
            raise ValueError("Unknown type")
        return cls._registry[name]()

VehicleProducer.register("car", Car)
VehicleProducer.register("motorcycle", Motorcycle)

if __name__ == "__main__":
    for key in ("car", "motorcycle"):
        vehicle = VehicleProducer.create(key)
        print(vehicle.start_engine())