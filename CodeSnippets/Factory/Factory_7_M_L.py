class ProductA:
    def __init__(self):
        self.name = "Product A"

class ProductB:
    def __init__(self):
        self.name = "Product B"

class ProductC:
    def __init__(self):
        self.name = "Product C"

class Factory:
    @staticmethod
    def create_product(name):
        if name == "A":
            return ProductA()
        elif name == "B":
            return ProductB()
        elif name == "C":
            return ProductC()
        else:
            raise ValueError("Invalid product name")

if __name__ == "__main__":
    print(Factory.create_product("A"))  # Output: <ProductA object at 0x10dee68d0>
    print(Factory.create_product("B"))  # Output: <ProductB object at 0x10dee7490>
    print(Factory.create_product("C"))  # Output: <ProductC object at 0x10dee8050>
    print(Factory.create_product("D"))  # Output: ValueError: Invalid product name