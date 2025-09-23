from abc import ABC, abstractmethod

class Beverage(ABC):
    @abstractmethod
    def get_description(self):
        pass

    @abstractmethod
    def cost(self):
        pass

class Coffee(Beverage):
    def get_description(self):
        return "Coffee"

    def cost(self):
        return 2.0

class Tea(Beverage):
    def get_description(self):
        return "Tea"

    def cost(self):
        return 1.5

class AddOn(Beverage):
    def __init__(self, beverage):
        self._beverage = beverage

    def get_description(self):
        return self._beverage.get_description()

    def cost(self):
        return self._beverage.cost()

class MilkAddOn(AddOn):
    def get_description(self):
        return self._beverage.get_description() + ", Milk"

    def cost(self):
        return self._beverage.cost() + 0.5

class SugarAddOn(AddOn):
    def get_description(self):
        return self._beverage.get_description() + ", Sugar"

    def cost(self):
        return self._beverage.cost() + 0.2

if __name__ == "__main__":
    try:
        base_coffee = Coffee()
        coffee_with_milk = MilkAddOn(base_coffee)
        coffee_with_milk_and_sugar = SugarAddOn(coffee_with_milk)
        
        print(f"{coffee_with_milk_and_sugar.get_description()}: ${coffee_with_milk_and_sugar.cost():.2f}")
        
        base_tea = Tea()
        tea_with_sugar = SugarAddOn(base_tea)
        print(f"{tea_with_sugar.get_description()}: ${tea_with_sugar.cost():.2f}")
    except Exception as e:
        print(f"Error: {e}")