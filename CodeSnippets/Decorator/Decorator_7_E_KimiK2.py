class Coffee:
    def cost(self):
        return 5
    def description(self):
        return "Coffee"

class Milk:
    def __init__(self, drink):
        self.drink = drink
    def cost(self):
        return self.drink.cost() + 2
    def description(self):
        return self.drink.description() + ", Milk"

class Sugar:
    def __init__(self, drink):
        self.drink = drink
    def cost(self):
        return self.drink.cost() + 1
    def description(self):
        return self.drink.description() + ", Sugar"

if __name__ == "__main__":
    drink = Coffee()
    drink = Milk(drink)
    drink = Sugar(drink)
    print(f"{drink.description()} - ${drink.cost()}")