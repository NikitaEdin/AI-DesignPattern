from abc import ABC, abstractmethod
from typing import Callable, Dict, Type

class Transport(ABC):
    @abstractmethod
    def deliver(self) -> str:
        pass

class Car(Transport):
    def __init__(self, capacity: int = 4):
        self.capacity = capacity
    def deliver(self) -> str:
        return f"Car delivering with capacity {self.capacity}"

class Bike(Transport):
    def __init__(self, electric: bool = False):
        self.electric = electric
    def deliver(self) -> str:
        mode = "electric bike" if self.electric else "bike"
        return f"{mode} delivering quickly"

class Truck(Transport):
    def __init__(self, tonnage: float = 5.0):
        self.tonnage = tonnage
    def deliver(self) -> str:
        return f"Truck delivering up to {self.tonnage} tons"

class TransportMaker:
    def __init__(self, reuse: bool = True):
        self._creators: Dict[str, Callable[..., Transport]] = {}
        self._cache: Dict[str, Transport] = {}
        self.reuse = reuse

    def register(self, key: str, creator: Callable[..., Transport]) -> None:
        if not callable(creator):
            raise TypeError("creator must be callable")
        self._creators[key] = creator

    def create(self, key: str, **kwargs) -> Transport:
        if self.reuse and key in self._cache:
            return self._cache[key]
        creator = self._creators.get(key)
        if creator is None:
            raise ValueError(f"Unknown transport type: {key}")
        instance = creator(**kwargs)
        if not isinstance(instance, Transport):
            raise TypeError("creator must return a Transport instance")
        if self.reuse:
            self._cache[key] = instance
        return instance

if __name__ == "__main__":
    maker = TransportMaker(reuse=True)
    maker.register("car", lambda capacity=4: Car(capacity=capacity))
    maker.register("bike", lambda electric=False: Bike(electric=electric))
    maker.register("truck", lambda tonnage=5.0: Truck(tonnage=tonnage))

    a = maker.create("car", capacity=5)
    b = maker.create("bike", electric=True)
    c = maker.create("truck", tonnage=10.0)
    d = maker.create("car")  # will return cached instance for "car"

    print(a.deliver())
    print(b.deliver())
    print(c.deliver())
    print(d.deliver())
    print("a is d:", a is d)