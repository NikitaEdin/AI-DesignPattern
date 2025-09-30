import abc
from typing import Optional

class Vehicle:
    def __init__(self):
        self._engine: Optional[str] = None
        self._wheels: int = 0
        self._color: Optional[str] = None
        self._gps: bool = False
        self._sunroof: bool = False
    
    @property
    def engine(self) -> Optional[str]:
        return self._engine
    
    @engine.setter
    def engine(self, value: str) -> None:
        self._engine = value
    
    @property
    def wheels(self) -> int:
        return self._wheels
    
    @wheels.setter
    def wheels(self, value: int) -> None:
        if value < 0:
            raise ValueError("Wheels cannot be negative")
        self._wheels = value
    
    @property
    def color(self) -> Optional[str]:
        return self._color
    
    @color.setter
    def color(self, value: str) -> None:
        self._color = value
    
    @property
    def gps(self) -> bool:
        return self._gps
    
    @gps.setter
    def gps(self, value: bool) -> None:
        self._gps = value
    
    @property
    def sunroof(self) -> bool:
        return self._sunroof
    
    @sunroof.setter
    def sunroof(self, value: bool) -> None:
        self._sunroof = value
    
    def __str__(self) -> str:
        return (f"Vehicle(engine={self._engine}, wheels={self._wheels}, "
                f"color={self._color}, gps={self._gps}, sunroof={self._sunroof})")

class VehicleCreator(abc.ABC):
    @abc.abstractmethod
    def configure_engine(self, engine: str) -> 'VehicleCreator':
        pass
    
    @abc.abstractmethod
    def configure_wheels(self, wheels: int) -> 'VehicleCreator':
        pass
    
    @abc.abstractmethod
    def configure_color(self, color: str) -> 'VehicleCreator':
        pass
    
    @abc.abstractmethod
    def configure_gps(self, enabled: bool) -> 'VehicleCreator':
        pass
    
    @abc.abstractmethod
    def configure_sunroof(self, enabled: bool) -> 'VehicleCreator':
        pass
    
    @abc.abstractmethod
    def create(self) -> Vehicle:
        pass

class StandardVehicleCreator(VehicleCreator):
    def __init__(self):
        self._vehicle = Vehicle()
    
    def configure_engine(self, engine: str) -> 'StandardVehicleCreator':
        self._vehicle.engine = engine
        return self
    
    def configure_wheels(self, wheels: int) -> 'StandardVehicleCreator':
        self._vehicle.wheels = wheels
        return self
    
    def configure_color(self, color: str) -> 'StandardVehicleCreator':
        self._vehicle.color = color
        return self
    
    def configure_gps(self, enabled: bool) -> 'StandardVehicleCreator':
        self._vehicle.gps = enabled
        return self
    
    def configure_sunroof(self, enabled: bool) -> 'StandardVehicleCreator':
        self._vehicle.sunroof = enabled
        return self
    
    def create(self) -> Vehicle:
        if not self._vehicle.engine:
            raise ValueError("Engine must be specified")
        if self._vehicle.wheels <= 0:
            raise ValueError("Must have at least one wheel")
        return self._vehicle

class Director:
    def __init__(self, creator: VehicleCreator):
        self._creator = creator
    
    def construct_sports_car(self) -> Vehicle:
        return (self._creator
                .configure_engine("V8")
                .configure_wheels(4)
                .configure_color("Red")
                .configure_gps(True)
                .configure_sunroof(True)
                .create())
    
    def construct_economy_car(self) -> Vehicle:
        return (self._creator
                .configure_engine("1.2L")
                .configure_wheels(4)
                .configure_color("White")
                .configure_gps(False)
                .configure_sunroof(False)
                .create())

if __name__ == "__main__":
    creator = StandardVehicleCreator()
    director = Director(creator)
    
    sports_car = director.construct_sports_car()
    print(sports_car)
    
    economy_car = director.construct_economy_car()
    print(economy_car)
    
    custom_motorcycle = (creator
                        .configure_engine("600cc")
                        .configure_wheels(2)
                        .configure_color("Black")
                        .configure_gps(True)
                        .configure_sunroof(False)
                        .create())
    print(custom_motorcycle)