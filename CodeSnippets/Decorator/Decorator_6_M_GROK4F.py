import abc

class Beverage(abc.ABC):
    @abc.abstractmethod
    def cost(self):
        pass

    @abc.abstractmethod
    def description(self):
        pass

class DarkRoast(Beverage):
    def cost(self):
        return 0.99

    def description(self):
        return "Dark Roast Coffee"

class MochaEnhancer(Beverage):
    def __init__(self, beverage):
        if beverage is None:
            raise ValueError("Beverage cannot be None")
        self._beverage = beverage

    def cost(self):
        return 0.20 + self._beverage.cost()

    def description(self):
        return self._beverage.description() + ", Mocha"

class WhipEnhancer(Beverage):
    def __init__(self, beverage):
        if beverage is None:
            raise ValueError("Beverage cannot be None")
        self._beverage = beverage

    def cost(self):
        return 0.15 + self._beverage.cost()

    def description(self):
        return self._beverage.description() + ", Whip"

if __name__ == "__main__":
    try:
        base = DarkRoast()
        enhanced = MochaEnhancer(base)
        final = WhipEnhancer(enhanced)
        print(f"{final.description()}: ${final.cost():.2f}")
    except ValueError as e:
        print(f"Error: {e}")