from abc import ABC, abstractmethod

class Beverage(ABC):
    @abstractmethod
    def cost(self):
        pass
    
    @abstractmethod
    def description(self):
        pass

class Coffee(Beverage):
    def cost(self):
        return 2.00
    
    def description(self):
        return "Coffee"

class BeverageWrapper(Beverage):
    def __init__(self, beverage):
        if not isinstance(beverage, Beverage):
            raise TypeError("Must wrap a Beverage object")
        self._beverage = beverage

class Milk(BeverageWrapper):
    def cost(self):
        return self._beverage.cost() + 0.50
    
    def description(self):
        return self._beverage.description() + ", Milk"

class Sugar(BeverageWrapper):
    def cost(self):
        return self._beverage.cost() + 0.25
    
    def description(self):
        return self._beverage.description() + ", Sugar"

class Whip(BeverageWrapper):
    def cost(self):
        return self._beverage.cost() + 0.75
    
    def description(self):
        return self._beverage.description() + ", Whipped Cream"

if __name__ == "__main__":
    try:
        basic_coffee = Coffee()
        print(f"{basic_coffee.description()}: ${basic_coffee.cost():.2f}")
        
        coffee_with_milk = Milk(basic_coffee)
        print(f"{coffee_with_milk.description()}: ${coffee_with_milk.cost():.2f}")
        
        deluxe_coffee = Whip(Sugar(Milk(Coffee())))
        print(f"{deluxe_coffee.description()}: ${deluxe_coffee.cost():.2f}")
        
    except TypeError as e:
        print(f"Error: {e}")