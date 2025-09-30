class Pizza:
    def __init__(self):
        self.crust = None
        self.sauce = None
        self.toppings = []
    
    def __str__(self):
        return f"{self.crust} crust, {self.sauce} sauce, {', '.join(self.toppings)}"

class PizzaMaker:
    def __init__(self):
        self.pizza = Pizza()
    
    def add_crust(self, crust_type):
        self.pizza.crust = crust_type
        return self
    
    def add_sauce(self, sauce_type):
        self.pizza.sauce = sauce_type
        return self
    
    def add_topping(self, topping):
        self.pizza.toppings.append(topping)
        return self
    
    def make(self):
        if not self.pizza.crust or not self.pizza.sauce:
            raise ValueError("Pizza must have crust and sauce")
        return self.pizza

if __name__ == "__main__":
    maker = PizzaMaker()
    try:
        pizza = maker.add_crust("thin").add_sauce("tomato").add_topping("cheese").add_topping("pepperoni").make()
        print(pizza)
    except ValueError as e:
        print(f"Error: {e}")