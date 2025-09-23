from abc import ABC, abstractmethod

class Pizza(ABC):
    @abstractmethod
    def get_description(self):
        pass

    @abstractmethod
    def get_cost(self):
        pass

class SimplePizza(Pizza):
    def get_description(self):
        return "Simple Pizza"

    def get_cost(self):
        return 10.0

class PizzaEnhancer(Pizza):
    def __init__(self, pizza):
        self._pizza = pizza

    def get_description(self):
        return self._pizza.get_description()

    def get_cost(self):
        return self._pizza.get_cost()

class CheeseEnhancer(PizzaEnhancer):
    def get_description(self):
        return self._pizza.get_description() + ", with Cheese"

    def get_cost(self):
        try:
            return self._pizza.get_cost() + 2.0
        except Exception:
            raise ValueError("Invalid cost calculation")

class OliveEnhancer(PizzaEnhancer):
    def get_description(self):
        return self._pizza.get_description() + ", with Olives"

    def get_cost(self):
        try:
            return self._pizza.get_cost() + 1.5
        except Exception:
            raise ValueError("Invalid cost calculation")

if __name__ == "__main__":
    base_pizza = SimplePizza()
    enhanced_pizza = CheeseEnhancer(base_pizza)
    final_pizza = OliveEnhancer(enhanced_pizza)
    print(f"{final_pizza.get_description()} costs ${final_pizza.get_cost():.2f}")