class Pizza:
    def __init__(self, dough, sauce, cheese, toppings):
        self.dough = dough
        self.sauce = sauce
        self.cheese = cheese
        self.toppings = toppings

    def __str__(self):
        toppings_str = ", ".join(self.toppings) if self.toppings else "none"
        return f"Pizza(Dough: {self.dough}, Sauce: {self.sauce}, Cheese: {self.cheese}, Toppings: {toppings_str})"

    def display(self):
        print(f"Preparing {self}...")
        print("Baking complete!")


class PizzaPreparer:
    def __init__(self):
        self.reset()

    def reset(self):
        self._dough = None
        self._sauce = None
        self._cheese = None
        self._toppings = []

    def set_dough(self, dough):
        if not isinstance(dough, str) or not dough.strip():
            raise ValueError("Dough must be a non-empty string")
        self._dough = dough
        return self

    def set_sauce(self, sauce):
        if not isinstance(sauce, str) or not sauce.strip():
            raise ValueError("Sauce must be a non-empty string")
        self._sauce = sauce
        return self

    def set_cheese(self, cheese):
        if not isinstance(cheese, str) or not cheese.strip():
            raise ValueError("Cheese must be a non-empty string")
        self._cheese = cheese
        return self

    def add_topping(self, topping):
        if not isinstance(topping, str) or not topping.strip():
            raise ValueError("Topping must be a non-empty string")
        self._toppings.append(topping)
        return self

    def add_toppings(self, toppings):
        if not isinstance(toppings, list):
            raise ValueError("Toppings must be a list of strings")
        for topping in toppings:
            self.add_topping(topping)
        return self

    def get_pizza(self):
        if self._dough is None:
            raise ValueError("Dough is required")
        if self._sauce is None:
            raise ValueError("Sauce is required")
        if self._cheese is None:
            raise ValueError("Cheese is required")
        pizza = Pizza(self._dough, self._sauce, self._cheese, self._toppings[:])
        self.reset()
        return pizza


class MargheritaOrchestrator:
    def __init__(self, preparer):
        self._preparer = preparer

    def construct_margherita(self):
        self._preparer.set_dough("thin crust") \
                      .set_sauce("tomato") \
                      .set_cheese("mozzarella") \
                      .add_topping("basil")
        return self._preparer.get_pizza()


class CustomPizzaOrchestrator:
    def __init__(self, preparer):
        self._preparer = preparer

    def construct_custom(self, dough, sauce, cheese, toppings=None):
        self._preparer.set_dough(dough) \
                      .set_sauce(sauce) \
                      .set_cheese(cheese)
        if toppings:
            self._preparer.add_toppings(toppings)
        return self._preparer.get_pizza()


if __name__ == "__main__":
    preparer = PizzaPreparer()

    # Using orchestrator for standard pizza
    margherita_orchestrator = MargheritaOrchestrator(preparer)
    margherita = margherita_orchestrator.construct_margherita()
    margherita.display()

    # Direct fluent usage for custom pizza
    custom = preparer.set_dough("thick crust") \
                     .set_sauce("bbq") \
                     .set_cheese("cheddar") \
                     .add_topping("chicken") \
                     .add_topping("onion") \
                     .get_pizza()
    custom.display()

    # Using orchestrator for another custom
    custom_orchestrator = CustomPizzaOrchestrator(preparer)
    veggie = custom_orchestrator.construct_custom("thin crust", "pesto", "feta", ["mushrooms", "peppers"])
    veggie.display()