import functools

class Coffee:
    def get_cost(self):
        raise NotImplementedError
    def get_description(self):
        raise NotImplementedError

class SimpleCoffee(Coffee):
    def get_cost(self):
        return 2.50
    def get_description(self):
        return "Simple coffee"

class CoffeeEnhancement(Coffee):
    def __init__(self, coffee):
        self._coffee = coffee
    def get_cost(self):
        return self._coffee.get_cost()
    def get_description(self):
        return self._coffee.get_description()

class Milk(CoffeeEnhancement):
    def get_cost(self):
        return self._coffee.get_cost() + 0.70
    def get_description(self):
        return self._coffee.get_description() + ", milk"

class Sugar(CoffeeEnhancement):
    def get_cost(self):
        return self._coffee.get_cost() + 0.20
    def get_description(self):
        return self._coffee.get_description() + ", sugar"

class Whip(CoffeeEnhancement):
    def get_cost(self):
        return self._coffee.get_cost() + 0.90
    def get_description(self):
        return self._coffee.get_description() + ", whip"

if __name__ == "__main__":
    beverage = SimpleCoffee()
    beverage = Milk(beverage)
    beverage = Sugar(beverage)
    beverage = Whip(beverage)
    print(f"{beverage.get_description()} => ${beverage.get_cost():.2f}")