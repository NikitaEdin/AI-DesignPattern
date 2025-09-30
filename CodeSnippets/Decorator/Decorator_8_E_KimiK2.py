class Coffee:
    def cost(self):
        return 5

class MilkAddon:
    def __init__(self, coffee):
        self.coffee = coffee
    
    def cost(self):
        return self.coffee.cost() + 2

class SugarAddon:
    def __init__(self, coffee):
        self.coffee = coffee
    
    def cost(self):
        return self.coffee.cost() + 1

if __name__ == "__main__":
    simple = Coffee()
    with_milk = MilkAddon(simple)
    with_milk_sugar = SugarAddon(with_milk)
    print(with_milk_sugar.cost())