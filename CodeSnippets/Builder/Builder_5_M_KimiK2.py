class Pizza:
    def __init__(self):
        self.size = None
        self.cheese = False
        self.pepperoni = False
        self.mushrooms = False
        self.extra_sauce = False

    def __str__(self):
        toppings = [k for k, v in {
            'cheese': self.cheese,
            'pepperoni': self.pepperoni,
            'mushrooms': self.mushrooms,
            'extra_sauce': self.extra_sauce
        }.items() if v]
        return f"{self.size}\" pizza with {', '.join(toppings) if toppings else 'no toppings'}"


class PizzaRecipe:
    def __init__(self):
        self.pizza = Pizza()

    def set_size(self, size: int):
        if size not in (10, 12, 14, 16):
            raise ValueError("Size must be 10, 12, 14, or 16 inches")
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

    def add_extra_sauce(self):
        self.pizza.extra_sauce = True
        return self

    def prepare(self) -> Pizza:
        if self.pizza.size is None:
            raise ValueError("Size must be set")
        return self.pizza


if __name__ == "__main__":
    try:
        p1 = PizzaRecipe().set_size(12).add_cheese().add_pepperoni().prepare()
        p2 = PizzaRecipe().set_size(16).add_mushrooms().add_extra_sauce().prepare()
        print(p1)
        print(p2)
    except ValueError as e:
        print("Error:", e)