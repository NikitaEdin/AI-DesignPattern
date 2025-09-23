class Vehicle:
    def __init__(self):
        self.engine = None
        self.seats = None
        self.color = None

    def __str__(self):
        return f"Vehicle: engine={self.engine}, seats={self.seats}, color={self.color}"

class VehicleConstructor:
    def __init__(self):
        self._vehicle = Vehicle()

    def add_engine(self, engine):
        self._vehicle.engine = engine
        return self

    def add_seats(self, seats):
        self._vehicle.seats = seats
        return self

    def set_color(self, color):
        self._vehicle.color = color
        return self

    def assemble(self):
        return self._vehicle

if __name__ == "__main__":
    constructor = VehicleConstructor()
    vehicle = constructor.add_engine("V6").add_seats(4).set_color("blue").assemble()
    print(vehicle)