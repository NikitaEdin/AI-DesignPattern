class Beverage:
    def get_cost(self):
        raise NotImplementedError
    
    def get_description(self):
        raise NotImplementedError

class Coffee(Beverage):
    def get_cost(self):
        return 2.00
    
    def get_description(self):
        return "Coffee"

class BeverageWrapper(Beverage):
    def __init__(self, beverage):
        if not isinstance(beverage, Beverage):
            raise TypeError("Expected Beverage instance")
        self._beverage = beverage
    
    def get_cost(self):
        return self._beverage.get_cost()
    
    def get_description(self):
        return self._beverage.get_description()

class MilkAddOn(BeverageWrapper):
    def get_cost(self):
        return self._beverage.get_cost() + 0.50
    
    def get_description(self):
        return self._beverage.get_description() + " + Milk"

class SugarAddOn(BeverageWrapper):
    def get_cost(self):
        return self._beverage.get_cost() + 0.25
    
    def get_description(self):
        return self._beverage.get_description() + " + Sugar"

class WhipCreamAddOn(BeverageWrapper):
    def get_cost(self):
        return self._beverage.get_cost() + 0.75
    
    def get_description(self):
        return self._beverage.get_description() + " + Whip Cream"

if __name__ == "__main__":
    coffee = Coffee()
    print(f"{coffee.get_description()}: ${coffee.get_cost():.2f}")
    
    coffee_with_milk = MilkAddOn(coffee)
    print(f"{coffee_with_milk.get_description()}: ${coffee_with_milk.get_cost():.2f}")
    
    fancy_coffee = WhipCreamAddOn(SugarAddOn(MilkAddOn(Coffee())))
    print(f"{fancy_coffee.get_description()}: ${fancy_coffee.get_cost():.2f}")