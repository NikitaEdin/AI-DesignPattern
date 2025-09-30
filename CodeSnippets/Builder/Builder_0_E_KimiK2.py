class Pizza:
    def __init__(self):
        self.size = None
        self.cheese = False
        self.pepperoni = False
        self.mushrooms = False
    def __str__(self):
        return f"Pizza(size={self.size}, cheese={self.cheese}, pepperoni={self.pepperoni}, mushrooms={self.mushrooms})"

class PizzaRecipe:
    def __init__(self):
        self.pizza = Pizza()
    def set_size(self, size):
        self.pizza.size = size
        return self
    def add_cheese(self):
        self.pizza.cheese = True
        return self
    def add_pepperoni(self):
        self.pizza.pepperoni = True
        return self
    def add_mushrooms(self):
        self.pizza.mushrooms = True
        return self
    def create(self):
        return self.pizza

if __name__ == "__main__":
    recipe = PizzaRecipe()
    my_pizza = recipe.set_size(12).add_cheese().add_pepperoni().create()
    print(my_pizza)