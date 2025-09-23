# Define the Product class
class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price
    
    def get_name(self):
        return self.name
    
    def get_price(self):
        return self.price
    
# Define the Builder class
class Builder:
    def __init__(self, product):
        self.product = product
    
    def set_name(self, name):
        self.product.name = name
    
    def set_price(self, price):
        self.product.price = price
    
# Define the Director class
class Director:
    def __init__(self, builder):
        self.builder = builder
    
    def build(self):
        self.builder.set_name("Product X")
        self.builder.set_price(10.99)
        return self.builder.product
    
# Test the code
if __name__ == "__main__":
    product = Director(Builder(Product("", ""))).build()
    print(f"Product name: {product.get_name()}")
    print(f"Product price: {product.get_price()}")