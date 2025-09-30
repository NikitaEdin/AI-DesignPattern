import time


class Pizza:
    def __init__(self):
        self.dough = None
        self.sauce = None
        self.toppings = []

    def __repr__(self):
        return f"Pizza({self.dough}, {self.sauce}, {self.toppings})"


class PizzaMaker:
    def __init__(self):
        self.pizza = Pizza()

    def add_dough(self, dough_type):
        if not dough_type:
            raise ValueError("Dough type cannot be empty")
        self.pizza.dough = dough_type
        return self

    def add_sauce(self, sauce_type):
        self.pizza.sauce = sauce_type
        return self

    def add_topping(self, topping):
        self.pizza.toppings.append(topping)
        return self

    def bake(self):
        if not self.pizza.dough:
            raise ValueError("Cannot bake without dough")
        return self.pizza


if __name__ == "__main__":
    pizza = (
        PizzaMaker()
        .add_dough("thin crust")
        .add_sauce("tomato")
        .add_topping("cheese")
        .add_topping("pepperoni")
        .bake()
    )
    print(pizza)