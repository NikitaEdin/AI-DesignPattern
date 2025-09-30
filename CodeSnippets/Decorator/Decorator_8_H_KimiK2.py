from abc import ABC, abstractmethod
import functools

class Beverage(ABC):
    @abstractmethod
    def cost(self) -> float: ...
    @abstractmethod
    def description(self) -> str: ...

class Espresso(Beverage):
    def cost(self) -> float: return 2.5
    def description(self) -> str: return "Espresso"

class Addon(Beverage):
    def __init__(self, beverage: Beverage):
        super().__init__()
        self._beverage = beverage

class Milk(Addon):
    def __init__(self, beverage: Beverage):
        super().__init__(beverage)
    def cost(self) -> float: return self._beverage.cost() + 0.5
    def description(self) -> str: return f"{self._beverage.description()}, Milk"

class Vanilla(Addon):
    def __init__(self, beverage: Beverage):
        super().__init__(beverage)
    def cost(self) -> float: return self._beverage.cost() + 0.7
    def description(self) -> str: return f"{self._beverage.description()}, Vanilla"

class SizeUp(Addon):
    def __init__(self, beverage: Beverage, multiplier: float = 1.5):
        super().__init__(beverage)
        if multiplier <= 1: raise ValueError("Multiplier must be > 1")
        self._multiplier = multiplier
    def cost(self) -> float: return self._beverage.cost() * self._multiplier
    def description(self) -> str: return f"{self._beverage.description()} (SizeUp)"

class Cache:
    _cache = {}
    @staticmethod
    def cached(func):
        @functools.wraps(func)
        def wrapper(self):
            key = (id(self), func.__name__)
            if key not in Cache._cache:
                Cache._cache[key] = func(self)
            return Cache._cache[key]
        return wrapper

class CachedAddon(Addon):
    def __init__(self, beverage: Beverage):
        super().__init__(beverage)
    @Cache.cached
    def cost(self) -> float: return self._beverage.cost() + 0.3
    @Cache.cached
    def description(self) -> str: return f"{self._beverage.description()}, Cached"

if __name__ == "__main__":
    drink = Espresso()
    drink = Milk(drink)
    drink = Vanilla(drink)
    drink = SizeUp(drink, 1.2)
    drink = CachedAddon(drink)
    print(f"{drink.description()} = ${drink.cost():.2f}")