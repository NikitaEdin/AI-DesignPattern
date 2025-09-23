class Beverage:
    def get_description(self):
        return "Unknown Beverage"

    def cost(self):
        return 0.0

class HouseBlend(Beverage):
    def get_description(self):
        return "House Blend Coffee"

    def cost(self):
        return 0.89

class Condiment(Beverage):
    def __init__(self, beverage):
        if beverage is None:
            raise ValueError("Beverage cannot be None")
        self._beverage = beverage

    def get_description(self):
        return self._beverage.get_description() + ", " + self._addition()

    def cost(self):
        return self._beverage.cost() + self._addition_cost()

    def _addition(self):
        raise NotImplementedError("Subclasses must implement _addition")

    def _addition_cost(self):
        raise NotImplementedError("Subclasses must implement _addition_cost")

class Mocha(Condiment):
    def _addition(self):
        return "Mocha"

    def _addition_cost(self):
        return 0.20

class Whip(Condiment):
    def _addition(self):
        return "Whip"

    def _addition_cost(self):
        return 0.45

if __name__ == "__main__":
    beverage = HouseBlend()
    print(f"{beverage.get_description()}: ${beverage.cost():.2f}")

    beverage = Mocha(beverage)
    print(f"{beverage.get_description()}: ${beverage.cost():.2f}")

    beverage = Mocha(beverage)
    beverage = Whip(beverage)
    print(f"{beverage.get_description()}: ${beverage.cost():.2f}")