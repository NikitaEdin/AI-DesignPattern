from abc import ABC, abstractmethod

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

class DarkRoast(Beverage):
    def get_description(self) -> str:
        return "Dark Roast Coffee"

    def cost(self) -> float:
        return 0.99

class BeverageModifier(Beverage):
    def __init__(self, beverage: Beverage):
        if not isinstance(beverage, Beverage):
            raise ValueError("Invalid beverage provided")
        if beverage is None:
            raise ValueError("Beverage cannot be None")
        self._beverage = beverage

    def get_description(self) -> str:
        return self._beverage.get_description()

    def cost(self) -> float:
        return self._beverage.cost()

class Mocha(BeverageModifier):
    def get_description(self) -> str:
        return super().get_description() + ", Mocha"

    def cost(self) -> float:
        return super().cost() + 0.20

class Whip(BeverageModifier):
    def get_description(self) -> str:
        return super().get_description() + ", Whip"

    def cost(self) -> float:
        return super().cost() + 0.15

class Soy(BeverageModifier):
    def get_description(self) -> str:
        return super().get_description() + ", Soy milk"

    def cost(self) -> float:
        return super().cost() + 0.10

if __name__ == "__main__":
    beverage = Espresso()
    print(f"{beverage.get_description()}: ${beverage.cost():.2f}")

    beverage = Mocha(beverage)
    print(f"{beverage.get_description()}: ${beverage.cost():.2f}")

    beverage = Whip(beverage)
    print(f"{beverage.get_description()}: ${beverage.cost():.2f}")

    print()

    beverage2 = DarkRoast()
    print(f"{beverage2.get_description()}: ${beverage2.cost():.2f}")

    beverage2 = Soy(beverage2)
    print(f"{beverage2.get_description()}: ${beverage2.cost():.2f}")

    beverage2 = Mocha(beverage2)
    beverage2 = Whip(beverage2)
    print(f"{beverage2.get_description()}: ${beverage2.cost():.2f}")