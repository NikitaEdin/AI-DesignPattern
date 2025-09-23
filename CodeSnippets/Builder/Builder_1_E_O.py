class Vehicle:
    def __init__(self): self.parts = []
    def __str__(self): return "Vehicle with: " + ", ".join(self.parts)

class Assembler:
    def __init__(self): self._product = Vehicle()
    def reset(self): self._product = Vehicle()
    def add_frame(self): self._product.parts.append("frame")
    def add_engine(self): self._product.parts.append("engine")
    def add_wheels(self): self._product.parts.append("wheels")
    def get_product(self):
        p = self._product; self.reset(); return p

class Coordinator:
    def assemble_minimal(self, a): a.add_frame(); a.add_engine()
    def assemble_full(self, a): a.add_frame(); a.add_engine(); a.add_wheels()

if __name__ == "__main__":
    a = Assembler(); c = Coordinator()
    c.assemble_minimal(a); v1 = a.get_product(); print(v1)
    c.assemble_full(a); v2 = a.get_product(); print(v2)