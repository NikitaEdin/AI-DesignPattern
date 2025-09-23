class Car:
    def __init__(self):
        self.engine = None
        self.wheels = None
        self.seats = None

    def __str__(self):
        return f"Car with {self.engine}, {self.wheels}, {self.seats}"

class CarAssembler:
    def __init__(self):
        self.car = Car()

    def set_engine(self):
        self.car.engine = "V8 engine"
        return self

    def set_wheels(self):
        self.car.wheels = "4 alloy wheels"
        return self

    def set_seats(self):
        self.car.seats = "leather seats"
        return self

    def get_car(self):
        return self.car

if __name__ == "__main__":
    my_car = (CarAssembler()
              .set_engine()
              .set_wheels()
              .set_seats()
              .get_car())
    print(my_car)