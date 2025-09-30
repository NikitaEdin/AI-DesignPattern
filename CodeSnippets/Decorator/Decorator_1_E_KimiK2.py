class Beverage:
    def cost(self):
        pass

class Coffee(Beverage):
    def cost(self):
        return 1.0

class Milk(Beverage):
    def __init__(self, beverage):
        self.beverage = beverage
    
    def cost(self):
        return self.beverage.cost() + 0.5

class Sugar(Beverage):
    def __init__(self, beverage):
        self.beverage = beverage
    
    def cost(self):
        return self.beverage.cost() + 0.2

if __name__ == "__main__":
    drink = Coffee()
    drink = Milk(drink)
    drink = Sugar(drink)
    print(drink.cost())