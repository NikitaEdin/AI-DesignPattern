class Product:
    def __init__(self): self.parts = []
    def add(self, p): self.parts.append(p)
    def show(self): print("Product parts:", ", ".join(self.parts))

class PartsMakerBase:
    def produce_part_a(self): raise NotImplementedError
    def produce_part_b(self): raise NotImplementedError
    def produce_part_c(self): raise NotImplementedError
    def get_result(self): raise NotImplementedError

class ConcretePartsMaker(PartsMakerBase):
    def __init__(self): self.product = Product()
    def produce_part_a(self): self.product.add("Frame")
    def produce_part_b(self): self.product.add("Engine")
    def produce_part_c(self): self.product.add("Wheels")
    def get_result(self): return self.product

class Coordinator:
    def construct(self, maker):
        maker.produce_part_a(); maker.produce_part_b(); maker.produce_part_c()
        return maker.get_result()

if __name__ == "__main__":
    maker = ConcretePartsMaker(); coordinator = Coordinator()
    product = coordinator.construct(maker); product.show()