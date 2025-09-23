class Pizza:
    def __init__(self):
        self.size = None
        self.crust = None
        self.toppings = []
    
    def __str__(self):
        return f"{self.size} pizza with {self.crust} crust and {', '.join(self.toppings)}"

class PizzaMaker:
    def __init__(self):
        self.pizza = Pizza()
    
    def set_size(self, size):
        self.pizza.size = size
        return self
    
    def set_crust(self, crust):
        self.pizza.crust = crust
        return self
    
    def add_topping(self, topping):
        self.pizza.toppings.append(topping)
        return self
    
    def create(self):
        return self.pizza

if __name__ == "__main__":
    pizza = PizzaMaker().set_size("large").set_crust("thin").add_topping("pepperoni").add_topping("mushrooms").create()
    print(pizza)