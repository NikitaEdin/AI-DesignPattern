from abc import ABC, abstractmethod

class Vehicle:
    def __init__(self):
        self.engine = None
        self.seats = None
        self.gps = False
        self.paint = None

    def __repr__(self):
        return f"Vehicle(engine={self.engine!r}, seats={self.seats!r}, gps={self.gps}, paint={self.paint!r})"

class AbstractCreator(ABC):
    @abstractmethod
    def set_engine(self, engine: str): ...
    @abstractmethod
    def set_seats(self, seats: int): ...
    @abstractmethod
    def enable_gps(self, enabled: bool = True): ...
    @abstractmethod
    def set_paint(self, color: str): ...
    @abstractmethod
    def produce(self) -> Vehicle: ...

class SportsCarCreator(AbstractCreator):
    def __init__(self):
        self.reset()

    def reset(self):
        self._product = Vehicle()
        return self

    def set_engine(self, engine: str):
        if not engine:
            raise ValueError("Engine must be specified")
        self._product.engine = engine
        return self

    def set_seats(self, seats: int):
        if seats not in (1, 2):
            raise ValueError("Sports model supports 1 or 2 seats")
        self._product.seats = seats
        return self

    def enable_gps(self, enabled: bool = True):
        self._product.gps = bool(enabled)
        return self

    def set_paint(self, color: str):
        if not color:
            raise ValueError("Paint color required")
        self._product.paint = color
        return self

    def produce(self) -> Vehicle:
        if not self._product.engine or not self._product.seats:
            raise ValueError("Incomplete specification: engine and seats required")
        finished = self._product
        self.reset()
        return finished

class OffroadCreator(AbstractCreator):
    def __init__(self):
        self.reset()

    def reset(self):
        self._product = Vehicle()
        return self

    def set_engine(self, engine: str):
        if "V6" not in engine and "V8" not in engine:
            raise ValueError("Offroad models require V6 or V8 engines")
        self._product.engine = engine
        return self

    def set_seats(self, seats: int):
        if seats < 2:
            raise ValueError("Offroad needs at least 2 seats")
        self._product.seats = seats
        return self

    def enable_gps(self, enabled: bool = True):
        self._product.gps = bool(enabled)
        return self

    def set_paint(self, color: str):
        self._product.paint = color or "matte green"
        return self

    def produce(self) -> Vehicle:
        if not self._product.engine or not self._product.seats:
            raise ValueError("Incomplete specification for offroad vehicle")
        finished = self._product
        self.reset()
        return finished

class Engineer:
    def create_sports(self, creator: AbstractCreator) -> Vehicle:
        return (creator.set_engine("V8 Turbo")
                      .set_seats(2)
                      .enable_gps(True)
                      .set_paint("red")
                      .produce())

    def create_explorer(self, creator: AbstractCreator) -> Vehicle:
        return (creator.set_engine("V6 Diesel")
                      .set_seats(5)
                      .enable_gps(False)
                      .set_paint("desert tan")
                      .produce())

if __name__ == "__main__":
    engineer = Engineer()
    sports_creator = SportsCarCreator()
    offroad_creator = OffroadCreator()

    sports_car = engineer.create_sports(sports_creator)
    print(sports_car)

    explorer = engineer.create_explorer(offroad_creator)
    print(explorer)

    try:
        incomplete = sports_creator.set_seats(2).produce()
    except ValueError as e:
        print("Error:", e)