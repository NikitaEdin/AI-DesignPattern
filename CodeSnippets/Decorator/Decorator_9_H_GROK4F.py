from abc import ABC, abstractmethod

class Beverage(ABC):
    @abstractmethod
    def get_description(self):
        pass

    @abstractmethod
    def cost(self):
        pass

class Espresso(Beverage):
    def get_description(self):
        return "Espresso"

    def cost(self):
        return 1.99

class DarkRoast(Beverage):
    def get_description(self):
        return "Dark Roast Coffee"

    def cost(self):
        return 0.99

class BeverageWrapper(Beverage):
    def __init__(self, beverage):
        if beverage is None:
            raise ValueError("Wrapped beverage cannot be None")
        self._beverage = beverage

    def get_description(self):
        return self._beverage.get_description()

    def cost(self):
        return self._beverage.cost()

class MochaWrapper(BeverageWrapper):
    def __init__(self, beverage):
        super().__init__(beverage)
        self._mocha_cost = 0.20

    def get_description(self):
        base_desc = super().get_description()
        return f"{base_desc}, Mocha"

    def cost(self):
        return super().cost() + self._mocha_cost

class WhipWrapper(BeverageWrapper):
    def __init__(self, beverage):
        super().__init__(beverage)
        self._whip_cost = 0.30

    def get_description(self):
        base_desc = super().get_description()
        return f"{base_desc}, Whip"

    def cost(self):
        return super().cost() + self._whip_cost

class SoyWrapper(BeverageWrapper):
    def __init__(self, beverage):
        super().__init__(beverage)
        self._soy_cost = 0.15

    def get_description(self):
        base_desc = super().get_description()
        return f"{base_desc}, Soy milk"

    def cost(self):
        return super().cost() + self._soy_cost

if __name__ == "__main__":
    beverage1 = Espresso()
    beverage1 = MochaWrapper(beverage1)
    beverage1 = WhipWrapper(beverage1)
    print(f"{beverage1.get_description()} ${beverage1.cost():.2f}")

    beverage2 = DarkRoast()
    beverage2 = SoyWrapper(beverage2)
    beverage2 = MochaWrapper(beverage2)
    beverage2 = WhipWrapper(beverage2)
    print(f"{beverage2.get_description()} ${beverage2.cost():.2f}")

    try:
        invalid_wrapper = BeverageWrapper(None)
    except ValueError as e:
        print(f"Error: {e}")