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
        return "Dark Roast"

    def cost(self):
        return 0.99

class HouseBlend(Beverage):
    def get_description(self):
        return "House Blend Coffee"

    def cost(self):
        return 0.89

class BeverageEnhancer(Beverage):
    def __init__(self, beverage):
        if beverage is None:
            raise ValueError("Base beverage cannot be None")
        self._beverage = beverage

    def get_description(self):
        return self._beverage.get_description()

    def cost(self):
        return self._beverage.cost()

class Milk(BeverageEnhancer):
    def get_description(self):
        return super().get_description() + ", Milk"

    def cost(self):
        return super().cost() + 0.20

class Mocha(BeverageEnhancer):
    def get_description(self):
        return super().get_description() + ", Mocha"

    def cost(self):
        return super().cost() + 0.45

class Whip(BeverageEnhancer):
    def get_description(self):
        return super().get_description() + ", Whip"

    def cost(self):
        return super().cost() + 0.30

if __name__ == "__main__":
    base = Espresso()
    print(f"{base.get_description()} ${base.cost():.2f}")

    enhanced = DarkRoast()
    enhanced = Mocha(enhanced)
    enhanced = Mocha(enhanced)
    enhanced = Whip(enhanced)
    print(f"{enhanced.get_description()} ${enhanced.cost():.2f}")

    blend = HouseBlend()
    blend = Milk(blend)
    print(f"{blend.get_description()} ${blend.cost():.2f}")

    try:
        invalid = Milk(None)
    except ValueError as e:
        print(f"Caught error: {e}")