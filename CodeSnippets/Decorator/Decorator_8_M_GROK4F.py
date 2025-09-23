class Beverage:
    def get_description(self):
        raise NotImplementedError("Subclasses must implement get_description")
    def cost(self):
        raise NotImplementedError("Subclasses must implement cost")

class Espresso(Beverage):
    def get_description(self):
        return "Espresso"
    def cost(self):
        return 1.99

class HouseBlend(Beverage):
    def get_description(self):
        return "House Blend"
    def cost(self):
        return 0.89

class BeverageWrapper(Beverage):
    def __init__(self, beverage):
        if not isinstance(beverage, Beverage):
            raise TypeError("Must wrap a Beverage")
        self._beverage = beverage
    def get_description(self):
        return self._beverage.get_description()
    def cost(self):
        return self._beverage.cost()

class Milk(BeverageWrapper):
    def get_description(self):
        return self._beverage.get_description() + ", Milk"
    def cost(self):
        return self._beverage.cost() + 0.10

class Mocha(BeverageWrapper):
    def get_description(self):
        return self._beverage.get_description() + ", Mocha"
    def cost(self):
        return self._beverage.cost() + 0.20

if __name__ == "__main__":
    espresso = Espresso()
    print(f"{espresso.get_description()} ${espresso.cost():.2f}")
    milk_espresso = Milk(espresso)
    print(f"{milk_espresso.get_description()} ${milk_espresso.cost():.2f}")
    mocha_milk_espresso = Mocha(milk_espresso)
    print(f"{mocha_milk_espresso.get_description()} ${mocha_milk_espresso.cost():.2f}")
    house_blend = HouseBlend()
    milk_house_blend = Milk(house_blend)
    print(f"{milk_house_blend.get_description()} ${milk_house_blend.cost():.2f}")