class CustomPizza:
    def __init__(self):
        self.size = None
        self.crust = None
        self.sauce = None
        self.toppings = []

    def __str__(self):
        if not self.size or not self.crust or not self.sauce:
            return "Incomplete pizza"
        return f"{self.size.title()} pizza with {self.crust} crust, {self.sauce} sauce, and toppings: {', '.join(self.toppings) or 'none'}"

class PizzaAssembler:
    def __init__(self):
        self.pizza = CustomPizza()

    def set_size(self, size):
        valid_sizes = ['small', 'medium', 'large']
        if size not in valid_sizes:
            raise ValueError(f"Size must be one of {valid_sizes}")
        self.pizza.size = size
        return self

    def set_crust(self, crust):
        if crust not in ['thin', 'thick', 'stuffed']:
            raise ValueError("Crust must be thin, thick, or stuffed")
        self.pizza.crust = crust
        return self

    def set_sauce(self, sauce):
        self.pizza.sauce = sauce
        return self

    def add_topping(self, topping):
        if isinstance(topping, str) and len(topping) > 0:
            self.pizza.toppings.append(topping)
        else:
            raise ValueError("Topping must be a non-empty string")
        return self

    def assemble(self):
        if not all([self.pizza.size, self.pizza.crust, self.pizza.sauce]):
            raise ValueError("Pizza requires size, crust, and sauce to assemble")
        return self.pizza

class PizzaShop:
    def __init__(self, assembler):
        self.assembler = assembler

    def create_veggie_pizza(self):
        return (self.assembler
                .set_size('medium')
                .set_crust('thin')
                .set_sauce('marinara')
                .add_topping('mushrooms')
                .add_topping('onions')
                .add_topping('bell peppers')
                .assemble())

if __name__ == "__main__":
    try:
        assembler = PizzaAssembler()
        shop = PizzaShop(assembler)
        pizza = shop.create_veggie_pizza()
        print(pizza)
    except ValueError as e:
        print(f"Error: {e}")