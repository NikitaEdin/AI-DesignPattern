class Pizza:
    def __init__(self):
        self.dough = None
        self.sauce = None
        self.topping = None

    def __str__(self):
        return f"Pizza: dough={self.dough}, sauce={self.sauce}, topping={self.topping}"

class PizzaConstructor:
    def __init__(self):
        self.product = Pizza()

    def add_dough(self, dough):
        self.product.dough = dough
        return self

    def add_sauce(self, sauce):
        self.product.sauce = sauce
        return self

    def add_topping(self, topping):
        self.product.topping = topping
        return self

    def create(self):
        return self.product

if __name__ == "__main__":
    constructor = PizzaConstructor()
    pizza = (constructor
             .add_dough("thin")
             .add_sauce("tomato")
             .add_topping("cheese")
             .create())
    print(pizza)