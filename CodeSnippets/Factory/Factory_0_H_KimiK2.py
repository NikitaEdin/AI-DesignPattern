from __future__ import annotations
import abc
import typing as t

class Vehicle(abc.ABC):
    @abc.abstractmethod
    def start_engine(self) -> str: ...
    @abc.abstractmethod
    def max_speed(self) -> int: ...

class Car(Vehicle):
    def start_engine(self) -> str:
        return "Car engine ignited"
    def max_speed(self) -> int:
        return 220

class Motorcycle(Vehicle):
    def start_engine(self) -> str:
        return "Motorcycle engine roaring"
    def max_speed(self) -> int:
        return 180

class Bicycle(Vehicle):
    def start_engine(self) -> str:
        return "Bicycle has no engine"
    def max_speed(self) -> int:
        return 40

class Creator(abc.ABC):
    registry: t.Dict[str, t.Type[Vehicle]] = {}
    @classmethod
    def register(cls, key: str, vehicle_cls: t.Type[Vehicle]) -> None:
        cls.registry[key] = vehicle_cls
    @abc.abstractmethod
    def _create(self, variant: str, **config) -> Vehicle: ...
    def build(self, variant: str, **config) -> Vehicle:
        if variant not in self.registry:
            raise ValueError(f"Unknown variant '{variant}'")
        return self._create(variant, **config)

class RoadBuilder(Creator):
    def _create(self, variant: str, **config) -> Vehicle:
        cls = self.registry[variant]
        instance = cls()
        for k, v in config.items():
            setattr(instance, k, v)
        return instance

if __name__ == "__main__":
    Creator.register("city", Car)
    Creator.register("sport", Motorcycle)
    Creator.register("eco", Bicycle)
    builder = RoadBuilder()
    vehicles = [
        builder.build("city", color="blue"),
        builder.build("sport", color="red"),
        builder.build("eco", gears=7)
    ]
    for v in vehicles:
        print(v.start_engine(), "| max:", v.max_speed())