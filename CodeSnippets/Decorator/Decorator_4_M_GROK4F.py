from abc import ABC, abstractmethod

class Beverage(ABC):
    @abstractmethod
    def cost(self):
        pass

    @abstractmethod
    def get_description(self):
        pass

class Espresso(Beverage):
    def cost(self):
        return 1.99

    def get_description(self):
        return "Espresso"

class BeverageWrapper(Beverage):
    def __init__(self, beverage):
        if beverage is None:
            raise ValueError("Beverage cannot be None")
        self._beverage = beverage

    def cost(self):
        return self._beverage.cost()

    def get_description(self):
        return self._beverage.get_description()

class Mocha(BeverageWrapper):
    def cost(self):
        return 0.20 + super().cost()

    def get_description(self):
        return super().get_description() + ", Mocha"

class Milk(BeverageWrapper):
    def cost(self):
        return 0.10 + super().cost()

    def get_description(self):
        return super().get_description() + ", Milk"

if __name__ == "__main__":
    beverage = Espresso()
    beverage = Mocha(beverage)
    beverage = Milk(beverage)
    print(f"{beverage.get_description()} ${beverage.cost():.2f}")