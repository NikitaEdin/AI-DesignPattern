class Product:
    def __init__(self, name):
        self.name = name

class Factory:
    @staticmethod
    def create_product(name):
        if name == "A":
            return Product("Product A")
        elif name == "B":
            return Product("Product B")
        else:
            raise ValueError("Invalid product name")

if __name__ == "__main__":
    product_a = Factory.create_product("A")
    print(product_a.name)

    try:
        product_c = Factory.create_product("C")
    except ValueError as e:
        print(e)