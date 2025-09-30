from abc import ABC, abstractmethod

class Coffee(ABC):
    @abstractmethod
    def cost(self) -> float:
        pass
    
    @abstractmethod
    def description(self) -> str:
        pass

class BasicCoffee(Coffee):
    def cost(self) -> float:
        return 2.0
    
    def description(self) -> str:
        return "Basic coffee"

class CoffeeEnhancement(Coffee):
    def __init__(self, base_coffee: Coffee):
        self._base_coffee = base_coffee
    
    def cost(self) -> float:
        return self._base_coffee.cost()
    
    def description(self) -> str:
        return self._base_coffee.description()

class MilkEnhancement(CoffeeEnhancement):
    def __init__(self, base_coffee: Coffee):
        super().__init__(base_coffee)
    
    def cost(self) -> float:
        return super().cost() + 0.5
    
    def description(self) -> str:
        return super().description() + ", milk"

class SugarEnhancement(CoffeeEnhancement):
    def __init__(self, base_coffee: Coffee):
        super().__init__(base_coffee)
    
    def cost(self) -> float:
        return super().cost() + 0.3
    
    def description(self) -> str:
        return super().description() + ", sugar"

class WhippedCreamEnhancement(CoffeeEnhancement):
    def __init__(self, base_coffee: Coffee):
        super().__init__(base_coffee)
    
    def cost(self) -> float:
        return super().cost() + 0.7
    
    def description(self) -> str:
        return super().description() + ", whipped cream"

if __name__ == "__main__":
    coffee = BasicCoffee()
    coffee = MilkEnhancement(coffee)
    coffee = SugarEnhancement(coffee)
    coffee = WhippedCreamEnhancement(coffee)
    
    print(f"Order: {coffee.description()}")
    print(f"Total cost: ${coffee.cost():.2f}")