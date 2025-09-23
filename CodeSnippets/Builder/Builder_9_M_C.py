class Pizza:
    def __init__(self):
        self.size = None
        self.crust = None
        self.toppings = []
        self.cheese = None
        self.sauce = None
    
    def __str__(self):
        return f"Pizza: {self.size}, {self.crust} crust, {self.cheese} cheese, {self.sauce} sauce, toppings: {', '.join(self.toppings)}"

class PizzaCreator:
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.pizza = Pizza()
        return self
    
    def set_size(self, size):
        if size not in ['small', 'medium', 'large']:
            raise ValueError("Size must be small, medium, or large")
        self.pizza.size = size
        return self
    
    def set_crust(self, crust):
        self.pizza.crust = crust
        return self
    
    def add_topping(self, topping):
        self.pizza.toppings.append(topping)
        return self
    
    def set_cheese(self, cheese):
        self.pizza.cheese = cheese
        return self
    
    def set_sauce(self, sauce):
        self.pizza.sauce = sauce
        return self
    
    def build(self):
        if not all([self.pizza.size, self.pizza.crust, self.pizza.cheese, self.pizza.sauce]):
            raise ValueError("Pizza must have size, crust, cheese, and sauce")
        result = self.pizza
        self.reset()
        return result

if __name__ == "__main__":
    creator = PizzaCreator()
    
    pizza1 = (creator
              .set_size("large")
              .set_crust("thin")
              .set_cheese("mozzarella")
              .set_sauce("tomato")
              .add_topping("pepperoni")
              .add_topping("mushrooms")
              .build())
    
    pizza2 = (creator
              .set_size("medium")
              .set_crust("thick")
              .set_cheese("cheddar")
              .set_sauce("bbq")
              .add_topping("chicken")
              .build())
    
    print(pizza1)
    print(pizza2)