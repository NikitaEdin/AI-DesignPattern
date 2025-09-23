class Coffee:
    def cost(self):
        return 2.0
    
    def description(self):
        return "Simple coffee"

class CoffeeEnhancer:
    def __init__(self, coffee):
        if not hasattr(coffee, 'cost') or not hasattr(coffee, 'description'):
            raise ValueError("Invalid coffee object")
        self._coffee = coffee
    
    def cost(self):
        return self._coffee.cost()
    
    def description(self):
        return self._coffee.description()

class MilkAddition(CoffeeEnhancer):
    def cost(self):
        return self._coffee.cost() + 0.5
    
    def description(self):
        return self._coffee.description() + ", with milk"

class SugarAddition(CoffeeEnhancer):
    def cost(self):
        return self._coffee.cost() + 0.2
    
    def description(self):
        return self._coffee.description() + ", with sugar"

class VanillaAddition(CoffeeEnhancer):
    def cost(self):
        return self._coffee.cost() + 0.7
    
    def description(self):
        return self._coffee.description() + ", with vanilla"

if __name__ == "__main__":
    basic_coffee = Coffee()
    print(f"{basic_coffee.description()}: ${basic_coffee.cost()}")
    
    coffee_with_milk = MilkAddition(basic_coffee)
    print(f"{coffee_with_milk.description()}: ${coffee_with_milk.cost()}")
    
    fancy_coffee = VanillaAddition(SugarAddition(MilkAddition(Coffee())))
    print(f"{fancy_coffee.description()}: ${fancy_coffee.cost()}")
    
    premium_coffee = MilkAddition(VanillaAddition(SugarAddition(Coffee())))
    print(f"{premium_coffee.description()}: ${premium_coffee.cost()}")