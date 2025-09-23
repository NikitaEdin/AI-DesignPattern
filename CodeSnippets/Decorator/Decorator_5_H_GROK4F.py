import abc

class Beverage(abc.ABC):
    @abc.abstractmethod
    def get_description(self) -> str:
        pass

    @abc.abstractmethod
    def get_cost(self) -> float:
        pass

class Espresso(Beverage):
    def get_description(self) -> str:
        return "Espresso"

    def get_cost(self) -> float:
        return 1.99

class DarkRoast(Beverage):
    def get_description(self) -> str:
        return "Dark Roast"

    def get_cost(self) -> float:
        return 0.99

class BeverageWrapper(Beverage):
    def __init__(self, beverage: Beverage = None):
        if beverage is None:
            self._beverage = Espresso()
        elif not isinstance(beverage, Beverage):
            raise TypeError("Wrapped item must be a Beverage instance")
        else:
            self._beverage = beverage

    def get_description(self) -> str:
        return self._beverage.get_description()

    def get_cost(self) -> float:
        return self._beverage.get_cost()

class MilkAddition(BeverageWrapper):
    def get_description(self) -> str:
        return super().get_description() + ", Milk"

    def get_cost(self) -> float:
        return super().get_cost() + 0.20

class MochaAddition(BeverageWrapper):
    def get_description(self) -> str:
        return super().get_description() + ", Mocha"

    def get_cost(self) -> float:
        return super().get_cost() + 0.45

class WhipAddition(BeverageWrapper):
    def get_description(self) -> str:
        return super().get_description() + ", Whip"

    def get_cost(self) -> float:
        return super().get_cost() + 0.30

if __name__ == "__main__":
    base = Espresso()
    print(f"{base.get_description()}: ${base.get_cost():.2f}")

    with_milk = MilkAddition(base)
    print(f"{with_milk.get_description()}: ${with_milk.get_cost():.2f}")

    with_mocha = MochaAddition(with_milk)
    print(f"{with_mocha.get_description()}: ${with_mocha.get_cost():.2f}")

    dark_with_whip = WhipAddition(DarkRoast())
    print(f"{dark_with_whip.get_description()}: ${dark_with_whip.get_cost():.2f}")

    try:
        invalid = BeverageWrapper("not a beverage")
    except TypeError as e:
        print(f"Error: {e}")

    none_base = BeverageWrapper(None)
    print(f"{none_base.get_description()}: ${none_base.get_cost():.2f}")