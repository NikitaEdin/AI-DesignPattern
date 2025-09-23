class Car:
    def __init__(self):
        self.engine = None
        self.wheels = None
        self.color = None
    
    def __str__(self):
        return f"Car: {self.color} with {self.engine} engine and {self.wheels} wheels"

class CarMaker:
    def __init__(self):
        self.car = Car()
    
    def set_engine(self, engine):
        self.car.engine = engine
        return self
    
    def set_wheels(self, wheels):
        self.car.wheels = wheels
        return self
    
    def set_color(self, color):
        self.car.color = color
        return self
    
    def build(self):
        return self.car

if __name__ == "__main__":
    maker = CarMaker()
    my_car = maker.set_engine("V8").set_wheels(4).set_color("red").build()
    print(my_car)