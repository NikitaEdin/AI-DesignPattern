from functools import wraps
import time
import logging

logging.basicConfig(level=logging.INFO)

class Beverage:
    def cost(self): pass
    def description(self): pass

class Espresso(Beverage):
    def cost(self): return 2.5
    def description(self): return "Espresso"

class HouseBlend(Beverage):
    def cost(self): return 1.2
    def description(self): return "House Blend"

class Addon(Beverage):
    def __init__(self, beverage):
        self._beverage = beverage
    def cost(self): return self._beverage.cost()
    def description(self): return self._beverage.description()

class Milk(Addon):
    def cost(self): return super().cost() + 0.5
    def description(self): return super().description() + ", Milk"

class Vanilla(Addon):
    def cost(self): return super().cost() + 0.7
    def description(self): return super().description() + ", Vanilla"

class Sugar(Addon):
    def cost(self): return super().cost() + 0.1
    def description(self): return super().description() + ", Sugar"

class CocoaPowder(Addon):
    def __init__(self, beverage, grams=5):
        super().__init__(beverage)
        self._grams = max(1, grams)
    def cost(self): return super().cost() + 0.05 * self._grams
    def description(self): return super().description() + f", Cocoa Powder({self._grams}g)"

class TimedBeverage(Beverage):
    def __init__(self, beverage):
        self._beverage = beverage
    @wraps(Beverage.cost)
    def cost(self):
        start = time.perf_counter()
        result = self._beverage.cost()
        elapsed = time.perf_counter() - start
        logging.info(f"Cost calculated in {elapsed:.6f}s")
        return result
    def description(self): return self._beverage.description()

if __name__ == "__main__":
    order = TimedBeverage(Vanilla(CocoaPowder(Milk(Espresso()), grams=3)))
    print(order.description(), "→", f"${order.cost():.2f}")
    order = TimedBeverage(Sugar(Sugar(HouseBlend())))
    print(order.description(), "→", f"${order.cost():.2f}")