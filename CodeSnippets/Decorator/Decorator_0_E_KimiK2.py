class Coffee:
    def cost(self):
        return 2

class Milk:
    def __init__(self, beverage):
        self.beverage = beverage
    def cost(self):
        return self.beverage.cost() + 0.5

class Sugar:
    def __init__(self, beverage):
        self.beverage = beverage
    def cost(self):
        return self.beverage.cost() + 0.2

if __name__ == "__main__":
    simple = Coffee()
    with_milk = Milk(simple)
    with_milk_and_sugar = Sugar(with_milk)
    print(with_milk_and_sugar.cost())