class Pizza:
    def get_description(self):
        pass

    def get_cost(self):
        pass

class SimplePizza(Pizza):
    def get_description(self):
        return "Simple Pizza"

    def get_cost(self):
        return 10.0

class CheeseTopping(Pizza):
    def __init__(self, pizza):
        if not isinstance(pizza, Pizza):
            raise ValueError("Must provide a valid Pizza instance")
        self._pizza = pizza

    def get_description(self):
        return f"{self._pizza.get_description()} with Cheese"

    def get_cost(self):
        return self._pizza.get_cost() + 3.0

class PepperoniTopping(Pizza):
    def __init__(self, pizza):
        if not isinstance(pizza, Pizza):
            raise ValueError("Must provide a valid Pizza instance")
        self._pizza = pizza

    def get_description(self):
        return f"{self._pizza.get_description()} with Pepperoni"

    def get_cost(self):
        return self._pizza.get_cost() + 5.0

if __name__ == "__main__":
    try:
        pizza = SimplePizza()
        pizza = CheeseTopping(pizza)
        pizza = PepperoniTopping(pizza)
        print(f"Description: {pizza.get_description()}")
        print(f"Cost: ${pizza.get_cost():.2f}")
    except ValueError as e:
        print(f"Error: {e}")