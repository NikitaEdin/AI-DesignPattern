import time

class Coffee:
    def cost(self):
        return 2.00
    def description(self):
        return "Basic coffee"

class Milk:
    def __init__(self, beverage):
        self.beverage = beverage
    def cost(self):
        return self.beverage.cost() + 0.50
    def description(self):
        return self.beverage.description() + ", milk"

class Sugar:
    def __init__(self, beverage):
        self.beverage = beverage
    def cost(self):
        return self.beverage.cost() + 0.25
    def description(self):
        return self.beverage.description() + ", sugar"

class Foam:
    def __init__(self, beverage):
        self.beverage = beverage
    def cost(self):
        return self.beverage.cost() + 0.30
    def description(self):
        return self.beverage.description() + ", foam"

if __name__ == "__main__":
    order = Coffee()
    order = Milk(order)
    order = Sugar(order)
    order = Foam(order)
    print(f"{order.description()} -> ${order.cost():.2f}")