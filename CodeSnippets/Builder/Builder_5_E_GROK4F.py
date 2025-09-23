class Pizza:
    def __init__(self):
        self.size = ""
        self.toppings = []

    def __str__(self):
        return f"Pizza(size='{self.size}', toppings={self.toppings})"

class PizzaMaker:
    def __init__(self):
        self.pizza = Pizza()

    def set_size(self, size):
        self.pizza.size = size
        return self

    def add_topping(self, topping):
        self.pizza.toppings.append(topping)
        return self

    def get_pizza(self):
        return self.pizza

if __name__ == "__main__":
    maker = PizzaMaker()
    pizza = maker.set_size("large").add_topping("cheese").add_topping("pepperoni").get_pizza()
    print(pizza)