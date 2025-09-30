class Pizza:
    def __init__(self):
        self.base = None
        self.cheese = None
        self.toppings = []

    def __str__(self):
        return f"Pizza(base={self.base}, cheese={self.cheese}, toppings={self.toppings})"


class PizzaRecipe:
    def __init__(self):
        self.pizza = Pizza()

    def set_base(self, base):
        self.pizza.base = base
        return self

    def set_cheese(self, cheese):
        self.pizza.cheese = cheese
        return self

    def add_topping(self, topping):
        self.pizza.toppings.append(topping)
        return self

    def get_pizza(self):
        return self.pizza


if __name__ == "__main__":
    p = PizzaRecipe()
    pizza = p.set_base("thin").set_cheese("mozzarella").add_topping("pepperoni").add_topping("mushrooms").get_pizza()
    print(pizza)