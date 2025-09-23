class Product:
    def __init__(self): self.parts = []
    def describe(self): return " + ".join(self.parts)

class SimpleAssembler:
    def __init__(self): self.reset()
    def reset(self): self.product = Product()
    def add_body(self): self.product.parts.append("body")
    def add_wheels(self): self.product.parts.append("wheels")
    def add_engine(self): self.product.parts.append("engine")
    def get_product(self): p = self.product; self.reset(); return p

class Director:
    def __init__(self, asm): self.asm = asm
    def construct_full(self): self.asm.reset(); self.asm.add_body(); self.asm.add_engine(); self.asm.add_wheels(); return self.asm.get_product()
    def construct_minimal(self): self.asm.reset(); self.asm.add_body(); self.asm.add_wheels(); return self.asm.get_product()

if __name__ == "__main__":
    asm = SimpleAssembler(); director = Director(asm)
    full = director.construct_full(); minimal = director.construct_minimal()
    print("Full:", full.describe())
    print("Minimal:", minimal.describe())