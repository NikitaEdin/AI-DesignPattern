class Car:
    def __init__(self):
        self.engine = None
        self.wheels = None
        self.color = None

class CarMaker:
    def __init__(self):
        self.car = Car()
    
    def add_engine(self, engine):
        self.car.engine = engine
        return self
    
    def add_wheels(self, wheels):
        self.car.wheels = wheels
        return self
    
    def add_color(self, color):
        self.car.color = color
        return self
    
    def build(self):
        return self.car

if __name__ == "__main__":
    maker = CarMaker()
    my_car = maker.add_engine("V8").add_wheels(4).add_color("red").build()
    print(f"Car: {my_car.engine} engine, {my_car.wheels} wheels, {my_car.color} color")