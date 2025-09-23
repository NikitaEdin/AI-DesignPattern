class Product:
    def __init__(self, name):
        self.name = name

class Car(Product):
    def __init__(self, name, color):
        super().__init__(name)
        self.color = color

class Truck(Product):
    def __init__(self, name, size):
        super().__init__(name)
        self.size = size

class VehicleFactory:
    @staticmethod
    def create_vehicle(type, name, *args):
        if type == "car":
            return Car(name, args[0])
        elif type == "truck":
            return Truck(name, args[0])
        else:
            raise ValueError("Invalid vehicle type")

if __name__ == "__main__":
    car = VehicleFactory.create_vehicle("car", "Ford Mustang", "red")
    print(car)  # Output: Ford Mustang (color=red)

    truck = VehicleFactory.create_vehicle("truck", "Big Rig", "large")
    print(truck)  # Output: Big Rig (size=large)