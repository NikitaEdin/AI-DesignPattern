class Product:
    def __init__(self):
        self.parts = []

    def add(self, part):
        self.parts.append(part)

    def __str__(self):
        return "Product parts: " + ", ".join(self.parts)


class MakerBase:
    def reset(self):
        raise NotImplementedError

    def assemble_part_a(self):
        raise NotImplementedError

    def assemble_part_b(self):
        raise NotImplementedError

    def get_product(self):
        raise NotImplementedError


class SimpleMaker(MakerBase):
    def __init__(self):
        self.reset()

    def reset(self):
        self._product = Product()

    def assemble_part_a(self):
        self._product.add("A")

    def assemble_part_b(self):
        self._product.add("B")

    def get_product(self):
        product = self._product
        self.reset()
        return product


class Director:
    def __init__(self, maker):
        self.maker = maker

    def construct_minimal(self):
        self.maker.reset()
        self.maker.assemble_part_a()
        return self.maker.get_product()

    def construct_full(self):
        self.maker.reset()
        self.maker.assemble_part_a()
        self.maker.assemble_part_b()
        return self.maker.get_product()


if __name__ == "__main__":
    maker = SimpleMaker()
    director = Director(maker)

    p1 = director.construct_minimal()
    print(p1)

    p2 = director.construct_full()
    print(p2)