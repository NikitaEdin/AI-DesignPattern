import abc

class Vehicle:
    def __init__(self, engine=None, wheels=0, color=None, is_electric=False):
        self.engine = engine
        self.wheels = wheels
        self.color = color
        self.is_electric = is_electric

    def __str__(self):
        return f"Vehicle: engine={self.engine}, wheels={self.wheels}, color={self.color}, electric={self.is_electric}"

class VehiclePreparer(abc.ABC):
    @abc.abstractmethod
    def add_engine(self, engine):
        pass

    @abc.abstractmethod
    def add_wheels(self, num):
        pass

    @abc.abstractmethod
    def add_color(self, color):
        pass

    @abc.abstractmethod
    def add_electric_mode(self, flag):
        pass

    @abc.abstractmethod
    def create_vehicle(self):
        pass

    @abc.abstractmethod
    def reset(self):
        pass

class AutomobilePreparer(VehiclePreparer):
    def __init__(self):
        self.reset()

    def add_engine(self, engine):
        valid_engines = ['gas', 'diesel', 'electric']
        if engine not in valid_engines:
            raise ValueError(f"Engine must be one of {valid_engines}")
        self._vehicle.engine = engine
        return self

    def add_wheels(self, num):
        if not isinstance(num, int) or num < 2 or num > 8:
            raise ValueError("Wheel count must be an integer between 2 and 8")
        self._vehicle.wheels = num
        return self

    def add_color(self, color):
        if not isinstance(color, str) or len(color) < 3:
            raise ValueError("Color must be a string with at least 3 characters")
        self._vehicle.color = color
        return self

    def add_electric_mode(self, flag):
        if not isinstance(flag, bool):
            raise ValueError("Electric mode must be a boolean")
        self._vehicle.is_electric = flag
        return self

    def create_vehicle(self):
        if self._vehicle.engine is None:
            raise ValueError("Engine is required")
        result = self._vehicle
        self.reset()
        return result

    def reset(self):
        self._vehicle = Vehicle()

class ProductionDirector:
    def __init__(self, preparer):
        self._preparer = preparer

    def assemble_sedan(self):
        self._preparer.add_engine('gas').add_wheels(4).add_color('silver').add_electric_mode(False)

    def assemble_electric_hatchback(self):
        self._preparer.add_engine('electric').add_wheels(4).add_color('green').add_electric_mode(True)

if __name__ == "__main__":
    preparer = AutomobilePreparer()
    director = ProductionDirector(preparer)
    director.assemble_sedan()
    sedan = preparer.create_vehicle()
    print(sedan)

    preparer = AutomobilePreparer()
    director.assemble_electric_hatchback()
    hatchback = preparer.create_vehicle()
    print(hatchback)

    custom = (AutomobilePreparer()
              .add_engine('diesel')
              .add_wheels(6)
              .add_color('blue')
              .add_electric_mode(False)
              .create_vehicle())
    print(custom)

    try:
        invalid = AutomobilePreparer().add_wheels(10).create_vehicle()
    except ValueError as e:
        print(f"Error: {e}")