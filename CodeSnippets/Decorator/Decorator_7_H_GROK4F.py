import abc

class Beverage(abc.ABC):
    @abc.abstractmethod
    def get_description(self) -> str:
        pass

    @abc.abstractmethod
    def get_cost(self) -> float:
        pass

class Espresso(Beverage):
    def get_description(self) -> str:
        return "Espresso"

    def get_cost(self) -> float:
        return 1.99

class HouseBlend(Beverage):
    def get_description(self) -> str:
        return "House Blend Coffee"

    def get_cost(self) -> float:
        return 0.89

class BeverageAdditive(Beverage):
    def __init__(self, beverage: Beverage):
        if beverage is None or not isinstance(beverage, Beverage):
            raise ValueError("Must provide a valid Beverage instance to wrap")
        self._wrapped = beverage

    def get_description(self) -> str:
        return self._wrapped.get_description()

    def get_cost(self) -> float:
        return self._wrapped.get_cost()

class Mocha(BeverageAdditive):
    def get_description(self) -> str:
        return self._wrapped.get_description() + ", Mocha"

    def get_cost(self) -> float:
        return self._wrapped.get_cost() + 0.20

class Whip(BeverageAdditive):
    def get_description(self) -> str:
        return self._wrapped.get_description() + ", Whip"

    def get_cost(self) -> float:
        return self._wrapped.get_cost() + 0.15

class Soy(BeverageAdditive):
    def get_description(self) -> str:
        return self._wrapped.get_description() + ", Soy Milk"

    def get_cost(self) -> float:
        return self._wrapped.get_cost() + 0.15

class SalesTax(BeverageAdditive):
    TAX_RATE = 0.08

    def get_description(self) -> str:
        return self._wrapped.get_description() + " (with sales tax)"

    def get_cost(self) -> float:
        base_cost = self._wrapped.get_cost()
        total = base_cost * (1 + self.TAX_RATE)
        return round(total, 2)

if __name__ == "__main__":
    print("Basic Espresso:")
    espresso = Espresso()
    print(f"{espresso.get_description()}: ${espresso.get_cost():.2f}")

    print("\nEspresso with Mocha:")
    mocha_espresso = Mocha(espresso)
    print(f"{mocha_espresso.get_description()}: ${mocha_espresso.get_cost():.2f}")

    print("\nEspresso with Mocha and Whip:")
    whip_mocha = Whip(mocha_espresso)
    print(f"{whip_mocha.get_description()}: ${whip_mocha.get_cost():.2f}")

    print("\nWith Sales Tax:")
    taxed = SalesTax(whip_mocha)
    print(f"{taxed.get_description()}: ${taxed.get_cost():.2f}")

    print("\nHouse Blend with Soy:")
    house_blend = HouseBlend()
    soy_house = Soy(house_blend)
    print(f"{soy_house.get_description()}: ${soy_house.get_cost():.2f}")

    print("\nEdge case handling:")
    try:
        invalid = Mocha(None)
    except ValueError as e:
        print(f"Error: {e}")

    try:
        class Invalid:
            pass
        invalid_obj = Invalid()
        bad_wrap = Mocha(invalid_obj)
    except ValueError as e:
        print(f"Error: {e}")