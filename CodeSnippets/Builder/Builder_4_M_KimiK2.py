class Pizza:
    def __init__(self):
        self.crust = None
        self.sauce = None
        self.toppings = []

    def __str__(self):
        return f"Pizza(crust={self.crust}, sauce={self.sauce}, toppings={self.toppings})"


class PizzaMaker:
    def __init__(self):
        self.pizza = Pizza()

    def set_crust(self, crust):
        self.pizza.crust = crust
        return self

    def set_sauce(self, sauce):
        self.pizza.sauce = sauce
        return self

    def add_topping(self, topping):
        if topping in self.pizza.toppings:
            raise ValueError("Duplicate topping")
        self.pizza.toppings.append(topping)
        return self

    def prepare(self):
        if not self.pizza.crust or not self.pizza.sauce:
            raise ValueError("Crust and sauce must be set")
        return self.pizza


class Director:
    def __init__(self, maker):
        self.maker = maker

    def make_margherita(self):
        return self.maker.set_crust("thin").set_sauce("tomato").add_topping("mozzarella").prepare()

    def make_pepperoni(self):
        return self.maker.set_crust("regular").set_sauce("tomato").add_topping("mozzarella").add_topping("pepperoni").prepare()


if __name__ == "__main__":
    maker = PizzaMaker()
    director = Director(maker)
    print(director.make_margherita())
    print(director.make_pepperoni())