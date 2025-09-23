class Car:
    def __init__(self):
        self.engine = None
        self.wheels = None
        self.color = 'white'
        self.extras = []

    def __str__(self):
        extras_str = ', '.join(self.extras) if self.extras else 'none'
        return f"Car: {self.engine} engine, {self.wheels} wheels, {self.color} color, extras: {extras_str}"

class CarAssembler:
    def __init__(self):
        self._car = Car()

    def set_engine(self, engine_type):
        self._car.engine = engine_type
        return self

    def set_wheels(self, num_wheels):
        if not isinstance(num_wheels, int) or num_wheels < 1 or num_wheels > 20:
            raise ValueError("Number of wheels must be a positive integer up to 20")
        self._car.wheels = num_wheels
        return self

    def set_color(self, color):
        if not isinstance(color, str) or len(color) < 1:
            raise ValueError("Color must be a non-empty string")
        self._car.color = color
        return self

    def add_extra(self, extra):
        if not isinstance(extra, str):
            raise ValueError("Extra must be a string")
        self._car.extras.append(extra)
        return self

    def reset(self):
        self._car = Car()
        return self

    def get_car(self):
        if self._car.engine is None:
            raise ValueError("Engine is required")
        if self._car.wheels is None:
            raise ValueError("Wheels are required")
        built_car = Car()
        built_car.engine = self._car.engine
        built_car.wheels = self._car.wheels
        built_car.color = self._car.color
        built_car.extras = self._car.extras[:]
        self.reset()
        return built_car

class CarManufacturer:
    def __init__(self, assembler):
        self._assembler = assembler

    def create_sports_car(self):
        return (self._assembler
                .set_engine("V8")
                .set_wheels(4)
                .set_color("red")
                .add_extra("spoiler")
                .add_extra("racing tires")
                .get_car())

    def create_family_car(self):
        return (self._assembler
                .set_engine("V6")
                .set_wheels(4)
                .set_color("silver")
                .add_extra("safety package")
                .add_extra("entertainment system")
                .get_car())

if __name__ == "__main__":
    assembler = CarAssembler()
    manufacturer = CarManufacturer(assembler)
    try:
        sports_car = manufacturer.create_sports_car()
        print(sports_car)
        family_car = manufacturer.create_family_car()
        print(family_car)
        assembler.set_engine("electric").set_wheels(4).get_car()
    except ValueError as e:
        print(f"Error: {e}")