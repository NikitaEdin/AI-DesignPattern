from abc import ABC, abstractmethod

class Beverage(ABC):
    @abstractmethod
    def get_description(self):
        pass

    @abstractmethod
    def get_cost(self):
        pass

class SimpleCoffee(Beverage):
    def get_description(self):
        return "Simple Coffee"

    def get_cost(self):
        return 2.0

class BeverageEnhancer(Beverage):
    def __init__(self, wrapped_beverage):
        self._wrapped_beverage = wrapped_beverage

    def get_description(self):
        return self._wrapped_beverage.get_description()

    def get_cost(self):
        return self._wrapped_beverage.get_cost()

class MilkAddition(BeverageEnhancer):
    def __init__(self, wrapped_beverage):
        super().__init__(wrapped_beverage)
        if not isinstance(wrapped_beverage, Beverage):
            raise ValueError("Wrapped item must be a Beverage")

    def get_description(self):
        return f"{self._wrapped_beverage.get_description()} with Milk"

    def get_cost(self):
        return self._wrapped_beverage.get_cost() + 0.5

class SugarAddition(BeverageEnhancer):
    def __init__(self, wrapped_beverage):
        super().__init__(wrapped_beverage)
        if not isinstance(wrapped_beverage, Beverage):
            raise ValueError("Wrapped item must be a Beverage")

    def get_description(self):
        return f"{self._wrapped_beverage.get_description()} with Sugar"

    def get_cost(self):
        return self._wrapped_beverage.get_cost() + 0.3

if __name__ == "__main__":
    coffee = SimpleCoffee()
    print(f"{coffee.get_description()}: ${coffee.get_cost():.2f}")

    coffee_with_milk = MilkAddition(coffee)
    print(f"{coffee_with_milk.get_description()}: ${coffee_with_milk.get_cost():.2f}")

    enhanced_coffee = SugarAddition(MilkAddition(coffee))
    print(f"{enhanced_coffee.get_description()}: ${enhanced_coffee.get_cost():.2f}")