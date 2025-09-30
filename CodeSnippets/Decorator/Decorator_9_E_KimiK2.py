class Coffee:
    def cost(self):
        return 5

class Milk:
    def __init__(self, drink):
        self.drink = drink
    def cost(self):
        return self.drink.cost() + 2

class Sugar:
    def __init__(self, drink):
        self.drink = drink
    def cost(self):
        return self.drink.cost() + 1

if __name__ == "__main__":
    coffee = Coffee()
    print(Milk(Sugar(coffee)).cost())