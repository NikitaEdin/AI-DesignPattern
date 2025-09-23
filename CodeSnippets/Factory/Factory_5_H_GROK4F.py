import abc

class Vehicle(abc.ABC):
    def __init__(self, color='white', model='default'):
        self.color = color
        self.model = model

    @abc.abstractmethod
    def start(self):
        pass

    def get_info(self):
        return f"{self.__class__.__name__}: {self.color} {self.model}"

class Car(Vehicle):
    def start(self):
        return f"Car {self.color} {self.model} starts with electronic key."

class Motorcycle(Vehicle):
    def start(self):
        return f"Motorcycle {self.color} {self.model} revs up with kickstart."

class Truck(Vehicle):
    def start(self):
        return f"Truck {self.color} {self.model} rumbles to life with diesel engine."

class VehicleProducer:
    def __init__(self):
        self._registry = {}
        self._default_class = None

    def register(self, type_name, cls):
        if not issubclass(cls, Vehicle):
            raise TypeError(f"{cls.__name__} must subclass Vehicle")
        self._registry[type_name.lower()] = cls

    def set_default(self, cls):
        if not issubclass(cls, Vehicle):
            raise TypeError(f"{cls.__name__} must subclass Vehicle")
        self._default_class = cls

    def create_vehicle(self, type_name, **kwargs):
        type_name = type_name.lower()
        cls = self._registry.get(type_name)
        if cls is None:
            if self._default_class:
                cls = self._default_class
            else:
                raise ValueError(f"Unknown vehicle type: {type_name}. Available: {list(self._registry.keys())}")
        try:
            instance = cls(**kwargs)
            if not isinstance(instance, Vehicle):
                raise TypeError("Created object must be a Vehicle instance")
            return instance
        except TypeError as e:
            raise ValueError(f"Invalid parameters for {type_name}: {e}")

if __name__ == "__main__":
    producer = VehicleProducer()
    producer.register("car", Car)
    producer.register("motorcycle", Motorcycle)
    producer.register("truck", Truck)
    producer.set_default(Car)

    car = producer.create_vehicle("car", color="blue", model="Sedan")
    print(car.get_info())
    print(car.start())

    motorcycle = producer.create_vehicle("bike", color="black")
    print(motorcycle.get_info())
    print(motorcycle.start())

    truck = producer.create_vehicle("truck", model="Heavy Duty")
    print(truck.get_info())
    print(truck.start())

    default_vehicle = producer.create_vehicle("van")
    print(f"Default: {default_vehicle.get_info()}")

    try:
        invalid = producer.create_vehicle("spaceship", invalid_param=42)
    except (ValueError, TypeError) as e:
        print(f"Error: {e}")