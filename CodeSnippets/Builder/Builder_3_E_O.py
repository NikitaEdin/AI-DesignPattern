class House:
    def __init__(self): self.parts = []
    def add(self, p): self.parts.append(p)
    def __str__(self): return "House with: " + ", ".join(self.parts)

class AssemblerBase:
    def reset(self): raise NotImplementedError
    def floor(self): raise NotImplementedError
    def walls(self): raise NotImplementedError
    def roof(self): raise NotImplementedError
    def result(self): raise NotImplementedError

class SimpleAssembler(AssemblerBase):
    def __init__(self): self.reset()
    def reset(self): self.product = House()
    def floor(self): self.product.add("floor")
    def walls(self): self.product.add("walls")
    def roof(self): self.product.add("roof")
    def result(self): r = self.product; self.reset(); return r

class Director:
    def set_assembler(self, a): self.a = a
    def construct(self):
        self.a.floor(); self.a.walls(); self.a.roof(); return self.a.result()

if __name__ == "__main__":
    assembler = SimpleAssembler(); director = Director(); director.set_assembler(assembler)
    print(director.construct())