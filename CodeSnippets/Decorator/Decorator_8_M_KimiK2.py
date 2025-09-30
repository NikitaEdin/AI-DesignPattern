class Coffee:
    def cost(self):
        return 2.0
    
    def description(self):
        return "Simple coffee"

class Milk:
    def __init__(self, beverage):
        self._beverage = beverage
    
    def cost(self):
        return self._beverage.cost() + 0.5
    
    def description(self):
        return self._beverage.description() + ", milk"

class Sugar:
    def __init__(self, beverage):
        self._beverage = beverage
    
    def cost(self):
        return self._beverage.cost() + 0.2
    
    def description(self):
        return self._beverage.description() + ", sugar"

class Whip:
    def __init__(self, beverage):
        self._beverage = beverage
    
    def cost(self):
        return self._beverage.cost() + 0.7
    
    def description(self):
        return self._beverage.description() + ", whip"

if __name__ == "__main__":
    order = Coffee()
    print(f"{order.description()}: ${order.cost()}")
    
    order = Milk(order)
    print(f"{order.description()}: ${order.cost()}")
    
    order = Sugar(order)
    print(f"{order.description()}: ${order.cost()}")
    
    order = Whip(order)
    print(f"{order.description()}: ${order.cost()}")