class Beverage:
    def get_description(self):
        raise NotImplementedError("Subclasses must implement get_description")

    def get_cost(self):
        raise NotImplementedError("Subclasses must implement get_cost")

class DarkRoast(Beverage):
    def get_description(self):
        return "Dark Roast Coffee"

    def get_cost(self):
        return 0.99

class Espresso(Beverage):
    def get_description(self):
        return "Espresso"

    def get_cost(self):
        return 1.99

class Condiment(Beverage):
    def __init__(self, beverage):
        if beverage is None:
            raise ValueError("Beverage cannot be None")
        self._beverage = beverage

    def get_description(self):
        return self._beverage.get_description()

    def get_cost(self):
        return self._beverage.get_cost()

class Mocha(Condiment):
    def get_description(self):
        return self._beverage.get_description() + ", Mocha"

    def get_cost(self):
        return self._beverage.get_cost() + 0.20

class Whip(Condiment):
    def get_description(self):
        return self._beverage.get_description() + ", Whip"

    def get_cost(self):
        return self._beverage.get_cost() + 0.15

if __name__ == "__main__":
    beverage = DarkRoast()
    print(f"{beverage.get_description()}: ${beverage.get_cost():.2f}")

    beverage = Mocha(beverage)
    print(f"{beverage.get_description()}: ${beverage.get_cost():.2f}")

    beverage = Mocha(beverage)
    beverage = Whip(beverage)
    print(f"{beverage.get_description()}: ${beverage.get_cost():.2f}")