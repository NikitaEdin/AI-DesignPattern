class Coffee:
    def cost(self):
        return 5

class Milk:
    def __init__(self, coffee):
        self.coffee = coffee
    def cost(self):
        return self.coffee.cost() + 2

class Sugar:
    def __init__(self, coffee):
        self.coffee = coffee
    def cost(self):
        return self.coffee.cost() + 1

if __name__ == "__main__":
    simple = Coffee()
    with_milk = Milk(simple)
    with_milk_and_sugar = Sugar(with_milk)
    print(with_milk_and_sugar.cost())