class Vehicle:
    def drive(self):
        raise NotImplementedError

class Car(Vehicle):
    def drive(self):
        return "Car is driving"

class Bike(Vehicle):
    def drive(self):
        return "Bike is riding"

class VehicleCreator:
    def make(self, kind):
        if kind == "car":
            return Car()
        if kind == "bike":
            return Bike()
        raise ValueError("Unknown vehicle type")

if __name__ == "__main__":
    creator = VehicleCreator()
    for key in ("car", "bike"):
        v = creator.make(key)
        print(v.drive())