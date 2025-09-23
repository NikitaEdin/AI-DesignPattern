class Pizza:
    def __init__(self):
        self.size = None
        self.crust = None
        self.sauce = None
        self.toppings = []

    def __str__(self):
        return f"Pizza: {self.size} inch, {self.crust} crust, {self.sauce} sauce, toppings: {', '.join(self.toppings)}"

class PizzaCrafter:
    def __init__(self):
        self.pizza = Pizza()

    def set_size(self, size):
        self.pizza.size = size
        return self

    def set_crust(self, crust):
        self.pizza.crust = crust
        return self

    def set_sauce(self, sauce):
        self.pizza.sauce = sauce
        return self

    def add_topping(self, topping):
        if topping not in self.pizza.toppings:
            self.pizza.toppings.append(topping)
        return self

    def get_pizza(self):
        if not self.pizza.size:
            raise ValueError("Pizza must have a size")
        if not self.pizza.toppings:
            self.pizza.toppings.append("cheese")
        return self.pizza

class PizzaOrderManager:
    def __init__(self, crafter):
        self.crafter = crafter

    def create_standard_pizza(self):
        self.crafter.set_size("12")
        self.crafter.set_crust("thin")
        self.crafter.set_sauce("tomato")
        self.crafter.add_topping("pepperoni")

    def create_veggie_pizza(self):
        self.crafter.set_size("14")
        self.crafter.set_crust("thick")
        self.crafter.set_sauce("pesto")
        self.crafter.add_topping("mushrooms")
        self.crafter.add_topping("bell peppers")

if __name__ == "__main__":
    crafter = PizzaCrafter()
    manager = PizzaOrderManager(crafter)
    manager.create_standard_pizza()
    pizza1 = crafter.get_pizza()
    print(pizza1)

    crafter = PizzaCrafter()
    manager = PizzaOrderManager(crafter)
    manager.create_veggie_pizza()
    pizza2 = crafter.get_pizza()
    print(pizza2)