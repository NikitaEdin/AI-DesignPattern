# Building objects with the Builder pattern in Python

class CarBuilder:
    """A builder for cars."""

    def __init__(self):
        self.car = {}

    def set_make(self, make):
        self.car['make'] = make

    def set_model(self, model):
        self.car['model'] = model

    def set_color(self, color):
        self.car['color'] = color

    def build(self):
        return Car(**self.car)

class Car:
    """A car."""

    def __init__(self, make, model, color):
        self.make = make
        self.model = model
        self.color = color

# Usage example
if __name__ == '__main__':
    builder = CarBuilder()
    builder.set_make('Toyota')
    builder.set_model('Camry')
    builder.set_color('red')

    car = builder.build()

    print(car)