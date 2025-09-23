class House:
    def __init__(self): self.parts = []
    def add(self, part): self.parts.append(part)
    def __str__(self): return "House parts: " + ", ".join(self.parts)
class CreatorBase:
    def reset(self): raise NotImplementedError
    def add_walls(self): raise NotImplementedError
    def add_roof(self): raise NotImplementedError
    def get_result(self): raise NotImplementedError
class HouseCreator(CreatorBase):
    def __init__(self): self.reset()
    def reset(self): self.product = House()
    def add_walls(self): self.product.add("walls")
    def add_roof(self): self.product.add("roof")
    def get_result(self):
        p = self.product; self.reset(); return p
class Foreman:
    def __init__(self, maker): self.maker = maker
    def construct_simple(self): self.maker.reset(); self.maker.add_walls()
    def construct_full(self): self.maker.reset(); self.maker.add_walls(); self.maker.add_roof()
if __name__ == "__main__":
    maker = HouseCreator()
    foreman = Foreman(maker)
    foreman.construct_simple(); print(maker.get_result())
    foreman.construct_full(); print(maker.get_result())