class Pizza:
    def __init__(self):
        self.dough = None
        self.sauce = None
        self.toppings = []

    def __str__(self):
        return f"{self.dough} dough, {self.sauce} sauce, {', '.join(self.toppings)}"

class PizzaMaker:
    def __init__(self):
        self.pizza = Pizza()

    def set_dough(self, dough):
        self.pizza.dough = dough
        return self

    def set_sauce(self, sauce):
        self.pizza.sauce = sauce
        return self

    def add_topping(self, topping):
        self.pizza.toppings.append(topping)
        return self

    def get_pizza(self):
        return self.pizza

if __name__ == "__main__":
    maker = PizzaMaker()
    pizza = (maker.set_dough("thin")
             .set_sauce("tomato")
             .add_topping("cheese")
             .add_topping("pepperoni")
             .get_pizza())
    print(str(pizza))