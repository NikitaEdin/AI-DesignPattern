from abc import ABC, abstractmethod

class Beverage(ABC):
    @abstractmethod
    def cost(self):
        pass

    @abstractmethod
    def get_description(self):
        pass

class Espresso(Beverage):
    def __init__(self):
        self._description = "Espresso"

    def get_description(self):
        return self._description

    def cost(self):
        return 1.99

class DarkRoast(Beverage):
    def __init__(self):
        self._description = "Dark Roast"

    def get_description(self):
        return self._description

    def cost(self):
        return 0.99

class HouseBlend(Beverage):
    def __init__(self):
        self._description = "House Blend"

    def get_description(self):
        return self._description

    def cost(self):
        return 0.89

class Milk(Beverage):
    def __init__(self, beverage):
        if not isinstance(beverage, Beverage):
            raise ValueError("Must provide a valid beverage")
        self._beverage = beverage

    def get_description(self):
        return self._beverage.get_description() + ", Milk"

    def cost(self):
        return self._beverage.cost() + 0.20

class Mocha(Beverage):
    def __init__(self, beverage):
        if not isinstance(beverage, Beverage):
            raise ValueError("Must provide a valid beverage")
        self._beverage = beverage

    def get_description(self):
        return self._beverage.get_description() + ", Mocha"

    def cost(self):
        return self._beverage.cost() + 0.30

class Whip(Beverage):
    def __init__(self, beverage):
        if not isinstance(beverage, Beverage):
            raise ValueError("Must provide a valid beverage")
        self._beverage = beverage

    def get_description(self):
        return self._beverage.get_description() + ", Whip"

    def cost(self):
        return self._beverage.cost() + 0.15

if __name__ == "__main__":
    espresso = Espresso()
    print(f"{espresso.get_description()}: ${espresso.cost():.2f}")

    dark_roast_with_milk = Milk(DarkRoast())
    print(f"{dark_roast_with_milk.get_description()}: ${dark_roast_with_milk.cost():.2f}")

    house_blend_with_mocha_and_whip = Whip(Mocha(HouseBlend()))
    print(f"{house_blend_with_mocha_and_whip.get_description()}: ${house_blend_with_mocha_and_whip.cost():.2f}")

    try:
        invalid = Milk(None)
    except ValueError as e:
        print(f"Error: {e}")