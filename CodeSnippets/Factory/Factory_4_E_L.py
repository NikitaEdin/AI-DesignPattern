class Product:
    def __init__(self, name):
        self.name = name

class Car(Product):
    def __init__(self, name):
        super().__init__(name)

class Truck(Product):
    def __init__(self, name):
        super().__init__(name)

class VehicleFactory:
    @staticmethod
    def create_product(name):
        if name == "Car":
            return Car(name)
        elif name == "Truck":
            return Truck(name)
        else:
            raise ValueError("Invalid product name")

if __name__ == "__main__":
    # Test the factory
    car = VehicleFactory.create_product("Car")
    print(car.name)  # Output: Car

    truck = VehicleFactory.create_product("Truck")
    print(truck.name)  # Output: Truck