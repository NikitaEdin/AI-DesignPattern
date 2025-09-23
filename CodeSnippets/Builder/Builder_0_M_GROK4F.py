class Pizza:
    def __init__(self):
        self.size = None
        self.crust_type = None
        self.toppings = []

    def __str__(self):
        toppings_str = ", ".join(self.toppings) if self.toppings else "none"
        return f"Pizza(size='{self.size}', crust='{self.crust_type}', toppings=[{toppings_str}])"

class PizzaPreparer:
    def __init__(self):
        self._pizza = Pizza()

    def set_size(self, size):
        if size not in ['small', 'medium', 'large']:
            raise ValueError("Invalid size")
        self._pizza.size = size
        return self

    def set_crust_type(self, crust_type):
        if crust_type not in ['thin', 'thick']:
            raise ValueError("Invalid crust type")
        self._pizza.crust_type = crust_type
        return self

    def add_topping(self, topping):
        if len(self._pizza.toppings) >= 10:
            raise ValueError("Too many toppings")
        self._pizza.toppings.append(topping)
        return self

    def prepare(self):
        if not self._pizza.size:
            raise ValueError("Size must be specified")
        if not self._pizza.toppings:
            raise ValueError("At least one topping required")
        return self._pizza

class PizzaSpecialist:
    def __init__(self, preparer):
        self._preparer = preparer

    def create_vegetarian(self):
        return (self._preparer
                .set_size('medium')
                .set_crust_type('thin')
                .add_topping('mushrooms')
                .add_topping('olives')
                .add_topping('bell peppers')
                .prepare())

    def create_meat_lovers(self):
        return (self._preparer
                .set_size('large')
                .set_crust_type('thick')
                .add_topping('pepperoni')
                .add_topping('sausage')
                .add_topping('bacon')
                .prepare())

if __name__ == "__main__":
    preparer = PizzaPreparer()
    specialist = PizzaSpecialist(preparer)

    try:
        veg_pizza = specialist.create_vegetarian()
        print(f"Vegetarian pizza: {veg_pizza}")

        meat_pizza = specialist.create_meat_lovers()
        print(f"Meat lovers pizza: {meat_pizza}")
    except ValueError as e:
        print(f"Error: {e}")