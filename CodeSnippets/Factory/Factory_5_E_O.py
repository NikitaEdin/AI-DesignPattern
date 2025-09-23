from abc import ABC, abstractmethod
class Product(ABC):
    @abstractmethod
    def do_action(self): ...
class ProductA(Product):
    def do_action(self): return "Action from Product A"
class ProductB(Product):
    def do_action(self): return "Action from Product B"
class Creator:
    def create(self, product_type):
        if product_type == "A": return ProductA()
        if product_type == "B": return ProductB()
        raise ValueError("Unknown product type")
if __name__ == "__main__":
    maker = Creator()
    for key in ("A", "B"):
        product = maker.create(key)
        print(product.do_action())