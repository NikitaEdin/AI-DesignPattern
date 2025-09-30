from abc import ABC, abstractmethod

class Beverage(ABC):
    @abstractmethod
    def cost(self) -> float:
        pass
    
    @abstractmethod
    def description(self) -> str:
        pass

class SimpleBeverage(Beverage):
    def cost(self) -> float:
        return 2.0
    
    def description(self) -> str:
        return "Simple beverage"

class BeverageEnhancer(Beverage):
    def __init__(self, beverage: Beverage):
        self._beverage = beverage
    
    def cost(self) -> float:
        return self._beverage.cost()
    
    def description(self) -> str:
        return self._beverage.description()

class Milk(BeverageEnhancer):
    def cost(self) -> float:
        return self._beverage.cost() + 0.5
    
    def description(self) -> str:
        return self._beverage.description() + ", milk"

class Vanilla(BeverageEnhancer):
    def cost(self) -> float:
        return self._beverage.cost() + 0.7
    
    def description(self) -> str:
        return self._beverage.description() + ", vanilla"

if __name__ == "__main__":
    beverage = SimpleBeverage()
    beverage = Milk(beverage)
    beverage = Vanilla(beverage)
    print(f"{beverage.description()}: ${beverage.cost():.2f}")