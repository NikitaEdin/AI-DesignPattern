import abc

class Beverage(abc.ABC):
    @abc.abstractmethod
    def cost(self) -> float:
        pass

    @abc.abstractmethod
    def get_description(self) -> str:
        pass

class Espresso(Beverage):
    def cost(self) -> float:
        return 1.99

    def get_description(self) -> str:
        return "Espresso"

class HouseBlend(Beverage):
    def cost(self) -> float:
        return 0.99

    def get_description(self) -> str:
        return "House Blend"

class DarkRoast(Beverage):
    def cost(self) -> float:
        return 0.99

    def get_description(self) -> str:
        return "Dark Roast"

class AddOn(Beverage):
    def __init__(self, beverage: Beverage):
        if not isinstance(beverage, Beverage):
            raise ValueError("Wrapped object must be a Beverage")
        self._beverage = beverage

    def get_description(self) -> str:
        return self._beverage.get_description()

    def cost(self) -> float:
        return self._beverage.cost()

class Milk(AddOn):
    def get_description(self) -> str:
        return f"{self._beverage.get_description()}, Milk"

    def cost(self) -> float:
        return self._beverage.cost() + 0.10

class Mocha(AddOn):
    def get_description(self) -> str:
        return f"{self._beverage.get_description()}, Mocha"

    def cost(self) -> float:
        return self._beverage.cost() + 0.20

class Whip(AddOn):
    def get_description(self) -> str:
        return f"{self._beverage.get_description()}, Whip"

    def cost(self) -> float:
        return self._beverage.cost() + 0.15

if __name__ == "__main__":
    beverage = Espresso()
    print(f"{beverage.get_description()}: ${beverage.cost():.2f}")

    beverage = HouseBlend()
    beverage = Mocha(beverage)
    beverage = Mocha(beverage)
    beverage = Whip(beverage)
    print(f"{beverage.get_description()}: ${beverage.cost():.2f}")

    beverage = DarkRoast()
    beverage = Milk(beverage)
    print(f"{beverage.get_description()}: ${beverage.cost():.2f}")

    try:
        invalid = Milk("not a beverage")
    except ValueError as e:
        print(f"Handled invalid wrapping: {e}")