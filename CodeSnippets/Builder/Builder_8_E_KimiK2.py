class Product:
    def __init__(self):
        self.parts = []
    def add(self, part):
        self.parts.append(part)
    def __str__(self):
        return f"Product: {', '.join(self.parts)}"

class Maker:
    def __init__(self):
        self.product = Product()
    def reset(self):
        self.product = Product()
    def set_part_a(self):
        self.product.add("PartA")
    def set_part_b(self):
        self.product.add("PartB")
    def get_result(self):
        return self.product

class Director:
    def __init__(self, maker):
        self.maker = maker
    def make_minimal(self):
        self.maker.reset()
        self.maker.set_part_a()
    def make_full(self):
        self.maker.reset()
        self.maker.set_part_a()
        self.maker.set_part_b()

if __name__ == "__main__":
    m = Maker()
    d = Director(m)
    d.make_minimal()
    print(m.get_result())
    d.make_full()
    print(m.get_result())