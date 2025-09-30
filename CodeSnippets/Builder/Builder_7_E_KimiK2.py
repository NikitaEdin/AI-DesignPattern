class Car:
    def __init__(self):
        self.engine = None
        self.wheels = None
        self.color = None
    
    def __str__(self):
        return f"Car: {self.engine}, {self.wheels} wheels, {self.color}"

class CarMaker:
    def __init__(self):
        self.car = Car()
    
    def add_engine(self, engine):
        self.car.engine = engine
        return self
    
    def add_wheels(self, count):
        self.car.wheels = count
        return self
    
    def paint(self, color):
        self.car.color = color
        return self
    
    def build(self):
        return self.car

if __name__ == "__main__":
    car = CarMaker().add_engine("V8").add_wheels(4).paint("red").build()
    print(car)