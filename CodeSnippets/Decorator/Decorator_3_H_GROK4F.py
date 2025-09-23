from abc import ABC, abstractmethod
from typing import Optional

class Beverage(ABC):
    @abstractmethod
    def get_description(self) -> str:
        pass

    @abstractmethod
    def cost(self) -> float:
        pass

class Espresso(Beverage):
    def get_description(self) -> str:
        return "Espresso"

    def cost(self) -> float:
        return 1.99

class HouseBlend(Beverage):
    def get_description(self) -> str:
        return "House Blend Coffee"

    def cost(self) -> float:
        return 0.89

class BeverageAddition(Beverage):
    def __init__(self, beverage: Optional[Beverage] = None):
        if beverage is None:
            raise ValueError("Must provide a valid beverage to wrap")
        self._beverage = beverage

    def get_description(self) -> str:
        return self._beverage.get_description()

    def cost(self) -> float:
        return self._beverage.cost()

class MilkAddition(BeverageAddition):
    def get_description(self) -> str:
        return self._beverage.get_description() + ", Milk"

    def cost(self) -> float:
        return self._beverage.cost() + 0.10

class MochaAddition(BeverageAddition):
    def get_description(self) -> str:
        return self._beverage.get_description() + ", Mocha"

    def cost(self) -> float:
        return self._beverage.cost() + 0.20

class WhipAddition(BeverageAddition):
    def get_description(self) -> str:
        return self._beverage.get_description() + ", Whip"

    def cost(self) -> float:
        return self._beverage.cost() + 0.15

class SoyAddition(BeverageAddition):
    def get_description(self) -> str:
        return self._beverage.get_description() + ", Soy"

    def cost(self) -> float:
        return self._beverage.cost() + 0.15

def calculate_with_tax(cost: float, tax_rate: float = 0.08) -> float:
    return cost * (1 + tax_rate)

if __name__ == "__main__":
    base = Espresso()
    enhanced = MilkAddition(base)
    further = MochaAddition(enhanced)
    final = WhipAddition(further)

    print(f"{final.get_description()}: ${final.cost():.2f}")
    print(f"With tax: ${calculate_with_tax(final.cost()):.2f}")

    try:
        invalid = MilkAddition(None)
    except ValueError as e:
        print(f"Error handled: {e}")

    stacked_blend = SoyAddition(HouseBlend())
    print(f"{stacked_blend.get_description()}: ${stacked_blend.cost():.2f}")