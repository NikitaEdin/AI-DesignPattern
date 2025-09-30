class Pizza:
    def __init__(self):
        self.size = None
        self.cheese = False
        self.pepperoni = False
        self.mushrooms = False
        self.onions = False
    
    def __str__(self):
        toppings = []
        if self.cheese: toppings.append("cheese")
        if self.pepperoni: toppings.append("pepperoni")
        if self.mushrooms: toppings.append("mushrooms")
        if self.onions: toppings.append("onions")
        return f"{self.size}\" pizza with {', '.join(toppings) if toppings else 'no toppings'}"

class PizzaCreator:
    def __init__(self):
        self.pizza = Pizza()
    
    def set_size(self, size):
        if size not in [10, 12, 14, 16]:
            raise ValueError("Invalid size")
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
    
    def add_onions(self):
        self.pizza.onions = True
        return self
    
    def create(self):
        if self.pizza.size is None:
            raise ValueError("Size must be set")
        return self.pizza

if __name__ == "__main__":
    creator = PizzaCreator()
    my_pizza = creator.set_size(14).add_cheese().add_pepperoni().create()
    print(my_pizza)
    
    veggie_pizza = PizzaCreator().set_size(12).add_cheese().add_mushrooms().add_onions().create()
    print(veggie_pizza)