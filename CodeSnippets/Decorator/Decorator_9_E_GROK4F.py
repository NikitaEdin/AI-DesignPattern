class Beverage:
    def cost(self):
        return 0

    def get_description(self):
        return "Unknown Beverage"

class Coffee(Beverage):
    def cost(self):
        return 5

    def get_description(self):
        return "Coffee"

class MilkAddOn(Beverage):
    def __init__(self, beverage):
        self._beverage = beverage

    def cost(self):
        return 2 + self._beverage.cost()

    def get_description(self):
        return self._beverage.get_description() + ", Milk"

class SugarAddOn(Beverage):
    def __init__(self, beverage):
        self._beverage = beverage

    def cost(self):
        return 1 + self._beverage.cost()

    def get_description(self):
        return self._beverage.get_description() + ", Sugar"

if __name__ == "__main__":
    coffee = Coffee()
    milk_coffee = MilkAddOn(coffee)
    sweet_milk_coffee = SugarAddOn(milk_coffee)
    print(sweet_milk_coffee.get_description() + ": $" + str(sweet_milk_coffee.cost()))