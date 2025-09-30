import math

class ShippingCost:
    def calculate(self, weight):
        raise NotImplementedError

class GroundShipping(ShippingCost):
    def calculate(self, weight):
        if weight <= 0:
            raise ValueError("Weight must be positive")
        return 5.0 + weight * 0.5

class AirShipping(ShippingCost):
    def calculate(self, weight):
        if weight <= 0:
            raise ValueError("Weight must be positive")
        return 20.0 + weight * 1.2

class ExpressShipping(ShippingCost):
    def calculate(self, weight):
        if weight <= 0:
            raise ValueError("Weight must be positive")
        return 50.0 + weight * 2.5

class Order:
    def __init__(self, weight, shipping_method):
        self.weight = weight
        self.shipping_method = shipping_method

    def get_total_shipping_cost(self):
        return self.shipping_method.calculate(self.weight)

if __name__ == "__main__":
    order1 = Order(10, GroundShipping())
    order2 = Order(10, AirShipping())
    order3 = Order(10, ExpressShipping())
    print(order1.get_total_shipping_cost())
    print(order2.get_total_shipping_cost())
    print(order3.get_total_shipping_cost())