class Product:
    def __init__(self): self.parts = []
    def add(self, p): self.parts.append(p)
    def __str__(self): return "Product with: " + ", ".join(self.parts)

class Assembler:
    def __init__(self): self.reset()
    def reset(self): self.product = Product()
    def part_a(self): self.product.add("A")
    def part_b(self): self.product.add("B")
    def get(self): r = self.product; self.reset(); return r

class Director:
    def __init__(self, assembler): self.assembler = assembler
    def build_min(self): self.assembler.part_a(); return self.assembler.get()
    def build_full(self): self.assembler.part_a(); self.assembler.part_b(); return self.assembler.get()

if __name__ == "__main__":
    asm = Assembler()
    d = Director(asm)
    print(d.build_min())
    print(d.build_full())