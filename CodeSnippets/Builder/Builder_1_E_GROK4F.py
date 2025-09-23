class Car:
    def __init__(self):
        self.components = {}

    def add_component(self, name, component):
        self.components[name] = component

    def __str__(self):
        return f"Car: {self.components}"

class CarAssembler:
    def __init__(self):
        self.car = Car()

    def add_engine(self, engine):
        self.car.add_component('engine', engine)

    def add_wheels(self, wheels):
        self.car.add_component('wheels', wheels)

    def get_car(self):
        return self.car

if __name__ == "__main__":
    assembler = CarAssembler()
    assembler.add_engine("V8")
    assembler.add_wheels(4)
    car = assembler.get_car()
    print(car)