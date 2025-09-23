```python
# A simple implementation of the Builder pattern in Python

class CarBuilder:
    """Builder class to construct a car"""

    def __init__(self):
        self.car = None

    def set_make(self, make):
        self.car = Car(make)

    def set_model(self, model):
        self.car.model = model

    def set_year(self, year):
        self.car.year = year

    def add_engine(self, engine):
        self.car.engine = engine

    def add_transmission(self, transmission):
        self.car.transmission = transmission

    def add_brakes(self, brakes):
        self.car.brakes = brakes

    def build(self):
        return self.car

class Car:
    """The car class"""

    def __init__(self, make):
        self.make = make
        self.model = None
        self.year = None
        self.engine = None
        self.transmission = None
        self.brakes = None

if __name__ == '__main__':
    # Example usage of the Builder pattern

    # Create a car builder
    builder = CarBuilder()

    # Set make, model, and year
    builder.set_make('Toyota')
    builder.set_model('Camry')
    builder.set_year(2015)

    # Add engine, transmission, and brakes
    builder.add_engine('V6')
    builder.add_transmission('Automatic')
    builder.add_brakes('Disc')

    # Build the car
    car = builder.build()

    print(car.make)  # Output: Toyota
    print(car.model)  # Output: Camry
    print(car.year)  # Output: 2015
    print(car.engine)  # Output: V6
    print(car.transmission)  # Output: Automatic
    print(car.brakes)  # Output: Disc
  ```