import functools
from typing import Protocol, runtime_checkable

@runtime_checkable
class Coffee(Protocol):
    def cost(self) -> float: ...
    def ingredients(self) -> str: ...

class BasicCoffee:
    def cost(self) -> float:
        return 2.50
    def ingredients(self) -> str:
        return "Coffee"

class AddonWrapper:
    def __init__(self, beverage: Coffee) -> None:
        self._beverage = beverage
    def cost(self) -> float:
        return self._beverage.cost()
    def ingredients(self) -> str:
        return self._beverage.ingredients()

class Milk(AddonWrapper):
    def __init__(self, beverage: Coffee, portion: float = 1.0) -> None:
        super().__init__(beverage)
        self._portion = max(0.1, min(2.0, portion))
    def cost(self) -> float:
        return self._beverage.cost() + 0.60 * self._portion
    def ingredients(self) -> str:
        return f"{self._beverage.ingredients()}, Milk"

class Vanilla(AddonWrapper):
    def __init__(self, beverage: Coffee, shots: int = 1) -> None:
        super().__init__(beverage)
        self._shots = max(1, min(5, shots))
    def cost(self) -> float:
        return self._beverage.cost() + 0.45 * self._shots
    def ingredients(self) -> str:
        return f"{self._beverage.ingredients()}, Vanilla"

class Whip(AddonWrapper):
    def __init__(self, beverage: Coffee, lite: bool = False) -> None:
        super().__init__(beverage)
        self._lite = lite
    def cost(self) -> float:
        return self._beverage.cost() + (0.35 if not self._lite else 0.25)
    def ingredients(self) -> str:
        return f"{self._beverage.ingredients()}, {'Lite' if self._lite else ''} Whip"

if __name__ == "__main__":
    espresso = BasicCoffee()
    print(f"{espresso.ingredients()} - ${espresso.cost():.2f}")

    latte = Milk(espresso, portion=1.5)
    print(f"{latte.ingredients()} - ${latte.cost():.2f}")

    fancy = Whip(Vanilla(Milk(BasicCoffee(), portion=0.8), shots=2), lite=True)
    print(f"{fancy.ingredients()} - ${fancy.cost():.2f}")