from abc import ABC, abstractmethod
import random
import threading

class Vehicle(ABC):
    @abstractmethod
    def start(self): ...
    @abstractmethod
    def specs(self) -> dict: ...

class Car(Vehicle):
    def __init__(self, model):
        self.model = model
    def start(self):
        return f"{self.model} car engine ignited"
    def specs(self):
        return {"wheels": 4, "type": "car"}

class Bike(Vehicle):
    def __init__(self, model):
        self.model = model
    def start(self):
        return f"{self.model} bike kick-started"
    def specs(self):
        return {"wheels": 2, "type": "bike"}

class Truck(Vehicle):
    def __init__(self, model):
        self.model = model
    def start(self):
        return f"{self.model} truck diesel engine roared"
    def specs(self):
        return {"wheels": 6, "type": "truck"}

class Creator:
    _lock = threading.Lock()
    _registry = {}
    _fallback = None

    @classmethod
    def register(cls, key, constructor):
        with cls._lock:
            cls._registry[key.lower()] = constructor

    @classmethod
    def set_fallback(cls, constructor):
        cls._fallback = constructor

    @classmethod
    def craft(cls, key, model):
        key = key.lower()
        with cls._lock:
            constructor = cls._registry.get(key, cls._fallback)
            if not constructor:
                raise ValueError(f"Unknown type '{key}'")
        return constructor(model)

Creator.register("car", Car)
Creator.register("bike", Bike)
Creator.register("truck", Truck)

if __name__ == "__main__":
    models = ["Tesla", "Yamaha", "Volvo"]
    types = ["car", "bike", "truck", "unknown"]
    for _ in range(5):
        t = random.choice(types)
        m = random.choice(models)
        try:
            v = Creator.craft(t, m)
            print(v.start(), v.specs())
        except ValueError as e:
            print(e)