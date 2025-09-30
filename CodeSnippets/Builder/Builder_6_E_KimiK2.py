class Product:
    def __init__(self):
        self.part_a = None
        self.part_b = None
    def __str__(self):
        return f"Product(a={self.part_a}, b={self.part_b})"

class Creator:
    def __init__(self):
        self.product = Product()
    def add_a(self, value):
        self.product.part_a = value
        return self
    def add_b(self, value):
        self.product.part_b = value
        return self
    def build(self):
        return self.product

if __name__ == "__main__":
    product = Creator().add_a("Alpha").add_b("Beta").build()
    print(product)