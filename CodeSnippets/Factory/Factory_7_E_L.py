class VehicleFactory:
    @staticmethod
    def create_vehicle(type) -> Vehicle:
        if type == "car":
            return Car()
        elif type == "truck":
            return Truck()
        else:
            raise ValueError("Invalid vehicle type")

class Vehicle:
    def __init__(self, make: str, model: str):
        self.make = make
        self.model = model

class Car(Vehicle):
    def __init__(self, make: str, model: str, year: int):
        super().__init__(make, model)
        self.year = year

class Truck(Vehicle):
    def __init__(self, make: str, model: str, payload: int):
        super().__init__(make, model)
        self.payload = payload

def main():
    vehicle_factory = VehicleFactory()
    car = vehicle_factory.create_vehicle("car")
    truck = vehicle_factory.create_vehicle("truck")
    print(car.make, car.model)
    print(truck.make, truck.model)

if __name__ == "__main__":
    main()