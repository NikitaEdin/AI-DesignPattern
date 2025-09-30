import functools

class Beverage:
    def cost(self):
        raise NotImplementedError
    def description(self):
        raise NotImplementedError

class Espresso(Beverage):
    def cost(self):
        return 2.5
    def description(self):
        return "Espresso"

class AddOn(Beverage):
    def __init__(self, drink):
        self._drink = drink

class Milk(AddOn):
    def cost(self):
        return self._drink.cost() + 0.5
    def description(self):
        return self._drink.description() + ", Milk"

class Sugar(AddOn):
    def cost(self):
        return self._drink.cost() + 0.2
    def description(self):
        return self._drink.description() + ", Sugar"

class Vanilla(AddOn):
    def cost(self):
        return self._drink.cost() + 0.7
    def description(self):
        return self._drink.description() + ", Vanilla"

if __name__ == "__main__":
    order = Espresso()
    order = Milk(order)
    order = Sugar(order)
    order = Vanilla(order)
    print(f"{order.description()} - ${order.cost():.2f}")