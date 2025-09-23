from abc import ABC, abstractmethod

class Beverage(ABC):
    @abstractmethod
    def cost(self):
        pass

    @abstractmethod
    def get_description(self):
        pass

class SimpleCoffee(Beverage):
    def cost(self):
        return 5.0

    def get_description(self):
        return "Simple Coffee"

class BeverageWrapper(ABC):
    def __init__(self, beverage):
        if not isinstance(beverage, Beverage):
            raise ValueError("Must wrap a valid Beverage instance")
        self._beverage = beverage

    def cost(self):
        return self._beverage.cost()

    def get_description(self):
        return self._beverage.get_description()

class MilkWrapper(BeverageWrapper):
    def cost(self):
        return super().cost() + 2.0

    def get_description(self):
        return super().get_description() + ", with Milk"

class SugarWrapper(BeverageWrapper):
    def cost(self):
        return super().cost() + 1.0

    def get_description(self):
        return super().get_description() + ", with Sugar"

if __name__ == "__main__":
    coffee = SimpleCoffee()
    print(f"{coffee.get_description()}: ${coffee.cost():.2f}")

    milk_coffee = MilkWrapper(coffee)
    print(f"{milk_coffee.get_description()}: ${milk_coffee.cost():.2f}")

    sweet_milk_coffee = SugarWrapper(milk_coffee)
    print(f"{sweet_milk_coffee.get_description()}: ${sweet_milk_coffee.cost():.2f}")