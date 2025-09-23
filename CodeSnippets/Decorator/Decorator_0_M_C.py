from abc import ABC, abstractmethod

class Coffee(ABC):
    @abstractmethod
    def cost(self):
        pass
    
    @abstractmethod
    def description(self):
        pass

class SimpleCoffee(Coffee):
    def cost(self):
        return 2.0
    
    def description(self):
        return "Simple coffee"

class CoffeeAddOn(Coffee):
    def __init__(self, coffee):
        if not isinstance(coffee, Coffee):
            raise ValueError("Invalid coffee object")
        self._coffee = coffee
    
    def cost(self):
        return self._coffee.cost()
    
    def description(self):
        return self._coffee.description()

class Milk(CoffeeAddOn):
    def cost(self):
        return self._coffee.cost() + 0.5
    
    def description(self):
        return self._coffee.description() + ", milk"

class Sugar(CoffeeAddOn):
    def cost(self):
        return self._coffee.cost() + 0.25
    
    def description(self):
        return self._coffee.description() + ", sugar"

class WhippedCream(CoffeeAddOn):
    def cost(self):
        return self._coffee.cost() + 0.75
    
    def description(self):
        return self._coffee.description() + ", whipped cream"

if __name__ == "__main__":
    coffee = SimpleCoffee()
    print(f"{coffee.description()}: ${coffee.cost():.2f}")
    
    coffee_with_milk = Milk(coffee)
    print(f"{coffee_with_milk.description()}: ${coffee_with_milk.cost():.2f}")
    
    fancy_coffee = WhippedCream(Sugar(Milk(SimpleCoffee())))
    print(f"{fancy_coffee.description()}: ${fancy_coffee.cost():.2f}")