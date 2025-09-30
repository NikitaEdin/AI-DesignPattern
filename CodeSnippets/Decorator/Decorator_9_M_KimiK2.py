import time

class Coffee:
    def cost(self):
        return 2.0
    def ingredients(self):
        return ["coffee"]

class MilkMixin:
    def __init__(self, beverage):
        self._beverage = beverage
    def cost(self):
        return self._beverage.cost() + 0.5
    def ingredients(self):
        return self._beverage.ingredients() + ["milk"]

class SugarMixin:
    def __init__(self, beverage):
        self._beverage = beverage
    def cost(self):
        return self._beverage.cost() + 0.2
    def ingredients(self):
        return self._beverage.ingredients() + ["sugar"]

class WhipMixin:
    def __init__(self, beverage):
        self._beverage = beverage
    def cost(self):
        return self._beverage.cost() + 0.7
    def ingredients(self):
        return self._beverage.ingredients() + ["whip"]

if __name__ == "__main__":
    simple = Coffee()
    print(f"Simple: ${simple.cost():.2f} - {simple.ingredients()}")
    with_milk = MilkMixin(Coffee())
    print(f"With milk: ${with_milk.cost():.2f} - {with_milk.ingredients()}")
    full = WhipMixin(SugarMixin(MilkMixin(Coffee())))
    print(f"Full: ${full.cost():.2f} - {full.ingredients()}")