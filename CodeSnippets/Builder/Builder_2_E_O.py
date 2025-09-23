class Product:
    def __init__(self): self.parts = []
    def __str__(self): return f"Product(parts={self.parts})"
class Creator:
    def reset(self): raise NotImplementedError
    def add_part_a(self): raise NotImplementedError
    def add_part_b(self): raise NotImplementedError
    def get_product(self): raise NotImplementedError
class ConcreteCreator(Creator):
    def __init__(self): self.reset()
    def reset(self): self._product = Product()
    def add_part_a(self): self._product.parts.append("A")
    def add_part_b(self): self._product.parts.append("B")
    def get_product(self):
        p=self._product; self.reset(); return p
class Director:
    def __init__(self, creator): self.creator=creator
    def construct_minimal(self):
        self.creator.add_part_a(); return self.creator.get_product()
    def construct_full(self):
        self.creator.add_part_a(); self.creator.add_part_b(); return self.creator.get_product()
if __name__=="__main__":
    c=ConcreteCreator(); d=Director(c)
    print(d.construct_minimal())
    print(d.construct_full())