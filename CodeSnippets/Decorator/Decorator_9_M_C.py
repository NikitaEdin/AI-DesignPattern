class Coffee:
    def get_cost(self):
        return 2.0
    
    def get_description(self):
        return "Simple coffee"

class CoffeeEnhancer:
    def __init__(self, coffee):
        if not hasattr(coffee, 'get_cost') or not hasattr(coffee, 'get_description'):
            raise ValueError("Invalid coffee object")
        self._coffee = coffee
    
    def get_cost(self):
        return self._coffee.get_cost()
    
    def get_description(self):
        return self._coffee.get_description()

class MilkAddOn(CoffeeEnhancer):
    def get_cost(self):
        return self._coffee.get_cost() + 0.5
    
    def get_description(self):
        return self._coffee.get_description() + ", milk"

class SugarAddOn(CoffeeEnhancer):
    def get_cost(self):
        return self._coffee.get_cost() + 0.2
    
    def get_description(self):
        return self._coffee.get_description() + ", sugar"

class WhippedCreamAddOn(CoffeeEnhancer):
    def get_cost(self):
        return self._coffee.get_cost() + 0.7
    
    def get_description(self):
        return self._coffee.get_description() + ", whipped cream"

if __name__ == "__main__":
    try:
        basic_coffee = Coffee()
        print(f"{basic_coffee.get_description()}: ${basic_coffee.get_cost():.2f}")
        
        coffee_with_milk = MilkAddOn(basic_coffee)
        print(f"{coffee_with_milk.get_description()}: ${coffee_with_milk.get_cost():.2f}")
        
        fancy_coffee = WhippedCreamAddOn(SugarAddOn(MilkAddOn(Coffee())))
        print(f"{fancy_coffee.get_description()}: ${fancy_coffee.get_cost():.2f}")
        
    except ValueError as e:
        print(f"Error: {e}")