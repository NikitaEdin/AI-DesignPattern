class Vehicle:
    def __init__(self, make, model, year):
        self.make = make
        self.model = model
        self.year = year

class Car(Vehicle):
    def __init__(self, make, model, year, num_doors):
        super().__init__(make, model, year)
        self.num_doors = num_doors

class Truck(Vehicle):
    def __init__(self, make, model, year, weight_capacity):
        super().__init__(make, model, year)
        self.weight_capacity = weight_capacity

class VehicleFactory:
    @staticmethod
    def create(vehicle_type, make, model, year, **kwargs):
        if vehicle_type == "car":
            return Car(make, model, year, kwargs.get("num_doors", 4))
        elif vehicle_type == "truck":
            return Truck(make, model, year, kwargs.get("weight_capacity", 1000))
        else:
            raise ValueError(f"Invalid vehicle type: {vehicle_type}")

def main():
    car = VehicleFactory.create("car", "Toyota", "Camry", 2015, num_doors=4)
    truck = VehicleFactory.create("truck", "Ford", "F-150", 2016, weight_capacity=3500)

    print(car)
    print(truck)

if __name__ == "__main__":
    main()