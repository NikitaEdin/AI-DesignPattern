from abc import ABC, abstractmethod

class Beverage(ABC):
    @abstractmethod
    def get_cost(self):
        pass
    
    @abstractmethod
    def get_description(self):
        pass

class Coffee(Beverage):
    def get_cost(self):
        return 2.00
    
    def get_description(self):
        return "Coffee"

class BeverageWrapper(Beverage):
    def __init__(self, beverage):
        if not isinstance(beverage, Beverage):
            raise ValueError("Invalid beverage type")
        self._beverage = beverage

class MilkWrapper(BeverageWrapper):
    def get_cost(self):
        return self._beverage.get_cost() + 0.50
    
    def get_description(self):
        return self._beverage.get_description() + ", Milk"

class SugarWrapper(BeverageWrapper):
    def get_cost(self):
        return self._beverage.get_cost() + 0.25
    
    def get_description(self):
        return self._beverage.get_description() + ", Sugar"

class WhipWrapper(BeverageWrapper):
    def get_cost(self):
        return self._beverage.get_cost() + 0.75
    
    def get_description(self):
        return self._beverage.get_description() + ", Whip"

if __name__ == "__main__":
    coffee = Coffee()
    print(f"{coffee.get_description()}: ${coffee.get_cost():.2f}")
    
    coffee_with_milk = MilkWrapper(coffee)
    print(f"{coffee_with_milk.get_description()}: ${coffee_with_milk.get_cost():.2f}")
    
    fancy_coffee = WhipWrapper(SugarWrapper(MilkWrapper(coffee)))
    print(f"{fancy_coffee.get_description()}: ${fancy_coffee.get_cost():.2f}")