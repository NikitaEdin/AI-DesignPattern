class Beverage:
    def get_description(self):
        pass
    def cost(self):
        pass

class DarkRoast(Beverage):
    def __init__(self):
        self._description = "Dark Roast Coffee"
    def get_description(self):
        return self._description
    def cost(self):
        return 0.99

class BeverageAddOn(Beverage):
    def __init__(self, beverage):
        self._beverage = beverage
    def get_description(self):
        return self._beverage.get_description()
    def cost(self):
        return self._beverage.cost()

class Mocha(BeverageAddOn):
    def get_description(self):
        return super().get_description() + ", Mocha"
    def cost(self):
        return super().cost() + 0.20

if __name__ == "__main__":
    beverage = DarkRoast()
    beverage = Mocha(beverage)
    print(beverage.get_description() + " $" + str(beverage.cost()))