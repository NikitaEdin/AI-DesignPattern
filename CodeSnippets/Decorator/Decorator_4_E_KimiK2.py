class Coffee:
    def cost(self):
        return 2

class Milk:
    def __init__(self, drink):
        self._drink = drink
    def cost(self):
        return self._drink.cost() + 1

class Sugar:
    def __init__(self, drink):
        self._drink = drink
    def cost(self):
        return self._drink.cost() + 0.5

if __name__ == "__main__":
    simple = Coffee()
    print(simple.cost())
    with_milk = Milk(simple)
    print(with_milk.cost())
    with_milk_sugar = Sugar(with_milk)
    print(with_milk_sugar.cost())