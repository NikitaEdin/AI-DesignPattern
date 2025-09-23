class ProductA:
    def __init__(self, name):
        self.name = name

class ProductB:
    def __init__(self, name):
        self.name = name

class Factory:
    @staticmethod
    def create_product(name):
        if name == "A":
            return ProductA("Product A")
        elif name == "B":
            return ProductB("Product B")
        else:
            raise ValueError("Invalid product name")

# Usage example
if __name__ == "__main__":
    a = Factory.create_product("A")
    print(a.name)
    b = Factory.create_product("B")
    print(b.name)