class ProductA:
    def __init__(self):
        self.name = "Product A"

class ProductB:
    def __init__(self):
        self.name = "Product B"

def create_product(type):
    if type == "A":
        return ProductA()
    elif type == "B":
        return ProductB()

# Usage example
if __name__ == "__main__":
    product1 = create_product("A")
    print(product1.name) # Output: Product A
    product2 = create_product("B")
    print(product2.name) # Output: Product B