class Pizza:
    def __init__(self):
        self.size = ""
        self.crust = ""
        self.toppings = []

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
    maker = PizzaMaker()
    pizza = maker.set_size("Large").set_crust("Thin").add_topping("Cheese").add_topping("Pepperoni").create()
    print(f"Pizza: {pizza.size}, {pizza.crust}, {pizza.toppings}")