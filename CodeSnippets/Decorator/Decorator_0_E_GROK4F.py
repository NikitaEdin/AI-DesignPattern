class Beverage:
    def cost(self):
        pass

class Coffee(Beverage):
    def cost(self):
        return 5

class Milk(Beverage):
    def __init__(self, beverage):
        self._beverage = beverage

    def cost(self):
        return self._beverage.cost() + 1

class Sugar(Beverage):
    def __init__(self, beverage):
        self._beverage = beverage

    def cost(self):
        return self._beverage.cost() + 0.5

if __name__ == "__main__":
    beverage = Coffee()
    print(f"Basic coffee cost: {beverage.cost()}")
    beverage = Milk(beverage)
    print(f"With milk: {beverage.cost()}")
    beverage = Sugar(beverage)
    print(f"With sugar: {beverage.cost()}")