from abc import ABC, abstractmethod

class Coffee(ABC):
    @abstractmethod
    def cost(self) -> float:
        pass

    @abstractmethod
    def description(self) -> str:
        pass

class BasicCoffee(Coffee):
    def cost(self) -> float:
        return 2.0

    def description(self) -> str:
        return "Basic coffee"

class CoffeeAddon(Coffee):
    def __init__(self, coffee: Coffee):
        self._coffee = coffee

class Milk(CoffeeAddon):
    def cost(self) -> float:
        return self._coffee.cost() + 0.5

    def description(self) -> str:
        return f"{self._coffee.description()}, milk"

class Sugar(CoffeeAddon):
    def cost(self) -> float:
        return self._coffee.cost() + 0.2

    def description(self) -> str:
        return f"{self._coffee.description()}, sugar"

class Vanilla(CoffeeAddon):
    def cost(self) -> float:
        return self._coffee.cost() + 0.7

    def description(self) -> str:
        return f"{self._coffee.description()}, vanilla"

if __name__ == "__main__":
    order = BasicCoffee()
    order = Milk(order)
    order = Sugar(order)
    order = Vanilla(order)
    print(f"{order.description()} - ${order.cost():.2f}")