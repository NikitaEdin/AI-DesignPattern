import time
import functools

class Coffee:
    def cost(self):
        return 2.0
    def description(self):
        return "Coffee"

class MilkAddOn:
    def __init__(self, beverage):
        self._beverage = beverage
    def cost(self):
        return self._beverage.cost() + 0.5
    def description(self):
        return self._beverage.description() + ", Milk"

class SugarAddOn:
    def __init__(self, beverage):
        self._beverage = beverage
    def cost(self):
        return self._beverage.cost() + 0.2
    def description(self):
        return self._beverage.description() + ", Sugar"

class WhipAddOn:
    def __init__(self, beverage):
        self._beverage = beverage
    def cost(self):
        return self._beverage.cost() + 0.7
    def description(self):
        return self._beverage.description() + ", Whip"

if __name__ == "__main__":
    simple = Coffee()
    print(f"{simple.description()}: ${simple.cost():.2f}")
    with_milk = MilkAddOn(simple)
    print(f"{with_milk.description()}: ${with_milk.cost():.2f}")
    with_milk_sugar = SugarAddOn(with_milk)
    print(f"{with_milk_sugar.description()}: ${with_milk_sugar.cost():.2f}")
    fully_loaded = WhipAddOn(with_milk_sugar)
    print(f"{fully_loaded.description()}: ${fully_loaded.cost():.2f}")