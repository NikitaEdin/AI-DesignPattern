from abc import ABC, abstractmethod
import functools
import time

class Coffee(ABC):
    @abstractmethod
    def cost(self) -> float: ...
    @abstractmethod
    def description(self) -> str: ...

class SimpleCoffee(Coffee):
    def cost(self) -> float: return 2.50
    def description(self) -> str: return "Simple coffee"

class CoffeeEnhancer(Coffee):
    def __init__(self, beverage: Coffee):
        self._beverage = beverage
    def cost(self) -> float: return self._beverage.cost()
    def description(self) -> str: return self._beverage.description()

class Milk(CoffeeEnhancer):
    def cost(self) -> float: return super().cost() + 0.70
    def description(self) -> str: return super().description() + ", milk"

class Vanilla(CoffeeEnhancer):
    def cost(self) -> float: return super().cost() + 0.90
    def description(self) -> str: return super().description() + ", vanilla"

class Whip(CoffeeEnhancer):
    def cost(self) -> float: return super().cost() + 0.50
    def description(self) -> str: return super().description() + ", whip"

class LoggingWrapper(CoffeeEnhancer):
    def __init__(self, beverage: Coffee, log_name: str = "LOG"):
        super().__init__(beverage)
        self._log_name = log_name
    def _log(self, method, *args, **kwargs):
        start = time.perf_counter()
        result = method(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"[{self._log_name}] {method.__name__} -> {result} ({elapsed*1000:.2f}ms)")
        return result
    def cost(self) -> float: return self._log(super().cost)
    def description(self) -> str: return self._log(super().description)

class CachingWrapper(CoffeeEnhancer):
    def __init__(self, beverage: Coffee):
        super().__init__(beverage)
        self._cache = {}
    def _cached(self, key, func, *args, **kwargs):
        if key not in self._cache:
            self._cache[key] = func(*args, **kwargs)
        return self._cache[key]
    def cost(self) -> float: return self._cached("cost", super().cost)
    def description(self) -> str: return self._cached("desc", super().description)

if __name__ == "__main__":
    drink = SimpleCoffee()
    drink = Milk(drink)
    drink = Vanilla(drink)
    drink = Whip(drink)
    drink = LoggingWrapper(drink)
    drink = CachingWrapper(drink)
    print(f"{drink.description()} -> ${drink.cost():.2f}")
    print(f"cached call: {drink.description()}")