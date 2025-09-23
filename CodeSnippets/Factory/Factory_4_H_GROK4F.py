from abc import ABC, abstractmethod
from typing import Callable

class Pizza(ABC):
    @abstractmethod
    def prepare(self) -> None:
        pass

    @abstractmethod
    def bake(self) -> None:
        pass

    @abstractmethod
    def get_name(self) -> str:
        pass

class CheesePizza(Pizza):
    def __init__(self):
        self._name = "Cheese Pizza"

    def prepare(self) -> None:
        print(f"Preparing dough and adding cheese for {self._name}")

    def bake(self) -> None:
        print(f"Baking {self._name} at 220°C for 15 minutes")

    def get_name(self) -> str:
        return self._name

class VeggiePizza(Pizza):
    def __init__(self):
        self._name = "Veggie Pizza"

    def prepare(self) -> None:
        print(f"Preparing dough and adding vegetables for {self._name}")

    def bake(self) -> None:
        print(f"Baking {self._name} at 220°C for 12 minutes")

    def get_name(self) -> str:
        return self._name

class PepperoniPizza(Pizza):
    def __init__(self):
        self._name = "Pepperoni Pizza"

    def prepare(self) -> None:
        print(f"Preparing dough and adding pepperoni for {self._name}")

    def bake(self) -> None:
        print(f"Baking {self._name} at 220°C for 14 minutes")

    def get_name(self) -> str:
        return self._name

class PizzaMaker:
    def __init__(self):
        self._recipes: dict[str, Callable[[], Pizza]] = {
            "cheese": self._create_cheese_pizza,
            "veggie": self._create_veggie_pizza,
        }

    def make_pizza(self, pizza_type: str) -> Pizza:
        if not isinstance(pizza_type, str) or not pizza_type.strip():
            raise ValueError("Pizza type must be a non-empty string")
        pizza_type = pizza_type.strip().lower()
        if pizza_type not in self._recipes:
            raise ValueError(f"Unknown pizza type: {pizza_type}")
        creator = self._recipes[pizza_type]
        pizza = creator()
        pizza.prepare()
        pizza.bake()
        return pizza

    def register_pizza(self, pizza_type: str, creator: Callable[[], Pizza]) -> None:
        if not isinstance(pizza_type, str) or not pizza_type.strip():
            raise ValueError("Pizza type must be a non-empty string")
        pizza_type = pizza_type.strip().lower()
        self._recipes[pizza_type] = creator

    def _create_cheese_pizza(self) -> Pizza:
        return CheesePizza()

    def _create_veggie_pizza(self) -> Pizza:
        return VeggiePizza()

if __name__ == "__main__":
    maker = PizzaMaker()
    try:
        cheese = maker.make_pizza("cheese")
        print(f"Created: {cheese.get_name()}\n")
        veggie = maker.make_pizza("Veggie")
        print(f"Created: {veggie.get_name()}\n")
        maker.register_pizza("pepperoni", PepperoniPizza)
        pepperoni = maker.make_pizza("pepperoni")
        print(f"Created: {pepperoni.get_name()}\n")
        invalid = maker.make_pizza("")
    except ValueError as e:
        print(f"Error: {e}")