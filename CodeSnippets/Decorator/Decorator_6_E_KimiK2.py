class Coffee:
    def cost(self):
        return 5

class Milk:
    def __init__(self, beverage):
        self.beverage = beverage
    
    def cost(self):
        return self.beverage.cost() + 2

class Sugar:
    def __init__(self, beverage):
        self.beverage = beverage
    
    def cost(self):
        return self.beverage.cost() + 1

if __name__ == "__main__":
    simple = Coffee()
    print(simple.cost())
    
    with_milk = Milk(simple)
    print(with_milk.cost())
    
    with_milk_and_sugar = Sugar(Milk(simple))
    print(with_milk_and_sugar.cost())