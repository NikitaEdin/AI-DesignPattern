import copy

class Pizza:
    def __init__(self, crust, sauce, toppings):
        self.crust = crust
        self.sauce = sauce
        self.toppings = toppings

    def __repr__(self):
        return f"Pizza(crust='{self.crust}', sauce='{self.sauce}', toppings={self.toppings})"

class PizzaConfigurator:
    def __init__(self):
        self._crust = None
        self._sauce = None
        self._toppings = set()
        self._allowed_crusts = {'thin', 'thick'}
        self._allowed_sauces = {'tomato', 'white'}
        self._allowed_toppings = {'cheese', 'pepperoni', 'mushrooms', 'basil', 'olives'}
        self._max_toppings = 5

    def set_crust(self, crust):
        if len(crust) < 3 or crust not in self._allowed_crusts:
            raise ValueError("Invalid crust type")
        self._crust = crust
        return self

    def set_sauce(self, sauce):
        if len(sauce) < 3 or sauce not in self._allowed_sauces:
            raise ValueError("Invalid sauce type")
        self._sauce = sauce
        return self

    def add_topping(self, topping):
        if self._sauce is None:
            raise ValueError("Sauce must be set before adding toppings")
        if len(topping) < 3 or topping not in self._allowed_toppings:
            raise ValueError("Invalid topping")
        if len(self._toppings) >= self._max_toppings:
            raise ValueError("Too many toppings")
        self._toppings.add(topping)
        return self

    def prepare(self):
        if self._crust is None or self._sauce is None:
            raise ValueError("Pizza must have crust and sauce")
        if not self._toppings:
            raise ValueError("Pizza must have at least one topping")
        toppings_list = sorted(list(self._toppings))
        return Pizza(self._crust, self._sauce, toppings_list)

class PizzaMenu:
    @staticmethod
    def configure_margherita(configurator):
        configurator.set_crust('thin').set_sauce('tomato').add_topping('cheese').add_topping('basil')
        return configurator

    @staticmethod
    def configure_pepperoni(configurator):
        configurator.set_crust('thick').set_sauce('tomato').add_topping('cheese').add_topping('pepperoni')
        return configurator

def main():
    try:
        # Custom pizza
        custom = (PizzaConfigurator()
                  .set_crust('thin')
                  .set_sauce('tomato')
                  .add_topping('mushrooms')
                  .add_topping('olives')
                  .prepare())
        print("Custom:", custom)

        # Predefined Margherita
        margherita = PizzaMenu.configure_margherita(PizzaConfigurator()).prepare()
        print("Margherita:", margherita)

        # Predefined Pepperoni
        pepperoni = PizzaMenu.configure_pepperoni(PizzaConfigurator()).prepare()
        print("Pepperoni:", pepperoni)

        # Invalid attempt (should raise error)
        invalid = PizzaConfigurator().add_topping('invalid')
    except ValueError as e:
        print("Error:", e)

if __name__ == "__main__":
    main()