class Pizza:
    def __init__(self):
        self.size = None
        self.cheese = False
        self.pepperoni = False
        self.mushrooms = False
    
    def __str__(self):
        return f"Pizza: {self.size}, Cheese: {self.cheese}, Pepperoni: {self.pepperoni}, Mushrooms: {self.mushrooms}"

class PizzaMaker:
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
    
    def make(self):
        return self.pizza

if __name__ == "__main__":
    maker = PizzaMaker()
    my_pizza = maker.set_size("Large").add_cheese().add_pepperoni().make()
    print(my_pizza)