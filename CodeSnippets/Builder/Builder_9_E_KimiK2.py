class Product:
    def __init__(self):
        self.part_a = None
        self.part_b = None
    
    def __str__(self):
        return f"Product: {self.part_a}, {self.part_b}"

class Creator:
    def __init__(self):
        self.product = Product()
    
    def set_part_a(self, value):
        self.product.part_a = value
        return self
    
    def set_part_b(self, value):
        self.product.part_b = value
        return self
    
    def build(self):
        return self.product

class Director:
    def __init__(self, creator):
        self.creator = creator
    
    def make_standard(self):
        return self.creator.set_part_a("Standard A").set_part_b("Standard B").build()
    
    def make_custom(self, a, b):
        return self.creator.set_part_a(a).set_part_b(b).build()

if __name__ == "__main__":
    creator = Creator()
    director = Director(creator)
    
    p1 = director.make_standard()
    p2 = director.make_custom("Custom A", "Custom B")
    
    print(p1)
    print(p2)