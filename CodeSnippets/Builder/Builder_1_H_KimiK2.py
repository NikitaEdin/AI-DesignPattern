import abc
from typing import Optional, List

class Vehicle:
    def __init__(self):
        self._engine: Optional[str] = None
        self._wheels: int = 0
        self._color: Optional[str] = None
        self._features: List[str] = []
        self._gps_enabled: bool = False
    
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
    def features(self) -> List[str]:
        return self._features.copy()
    
    def add_feature(self, feature: str) -> None:
        self._features.append(feature)
    
    @property
    def gps_enabled(self) -> bool:
        return self._gps_enabled
    
    @gps_enabled.setter
    def gps_enabled(self, value: bool) -> None:
        self._gps_enabled = value
    
    def __str__(self) -> str:
        return (f"Vehicle(engine={self._engine}, wheels={self._wheels}, "
                f"color={self._color}, features={self._features}, "
                f"gps={self._gps_enabled})")

class VehicleAssembler(abc.ABC):
    @abc.abstractmethod
    def configure_engine(self, engine_type: str) -> 'VehicleAssembler':
        pass
    
    @abc.abstractmethod
    def configure_wheels(self, count: int) -> 'VehicleAssembler':
        pass
    
    @abc.abstractmethod
    def paint(self, color: str) -> 'VehicleAssembler':
        pass
    
    @abc.abstractmethod
    def add_feature(self, feature: str) -> 'VehicleAssembler':
        pass
    
    @abc.abstractmethod
    def enable_gps(self) -> 'VehicleAssembler':
        pass
    
    @abc.abstractmethod
    def create(self) -> Vehicle:
        pass

class StandardVehicleAssembler(VehicleAssembler):
    def __init__(self):
        self._vehicle = Vehicle()
    
    def configure_engine(self, engine_type: str) -> 'StandardVehicleAssembler':
        self._vehicle.engine = engine_type
        return self
    
    def configure_wheels(self, count: int) -> 'StandardVehicleAssembler':
        self._vehicle.wheels = count
        return self
    
    def paint(self, color: str) -> 'StandardVehicleAssembler':
        self._vehicle.color = color
        return self
    
    def add_feature(self, feature: str) -> 'StandardVehicleAssembler':
        self._vehicle.add_feature(feature)
        return self
    
    def enable_gps(self) -> 'StandardVehicleAssembler':
        self._vehicle.gps_enabled = True
        return self
    
    def create(self) -> Vehicle:
        if self._vehicle.wheels == 0:
            raise ValueError("Vehicle must have wheels")
        if not self._vehicle.engine:
            raise ValueError("Vehicle must have an engine")
        return self._vehicle

class Director:
    def __init__(self, assembler: VehicleAssembler):
        self._assembler = assembler
    
    def construct_sports_car(self) -> Vehicle:
        return (self._assembler
                .configure_engine("V8")
                .configure_wheels(4)
                .paint("Red")
                .add_feature("Spoiler")
                .add_feature("Leather Seats")
                .enable_gps()
                .create())
    
    def construct_motorcycle(self) -> Vehicle:
        return (self._assembler
                .configure_engine("V2")
                .configure_wheels(2)
                .paint("Black")
                .add_feature("Helmet Holder")
                .create())

if __name__ == "__main__":
    assembler = StandardVehicleAssembler()
    director = Director(assembler)
    
    sports_car = director.construct_sports_car()
    print(sports_car)
    
    motorcycle = director.construct_motorcycle()
    print(motorcycle)
    
    custom_vehicle = (StandardVehicleAssembler()
                     .configure_engine("Electric")
                     .configure_wheels(3)
                     .paint("Blue")
                     .add_feature("Solar Panel")
                     .enable_gps()
                     .create())
    print(custom_vehicle)