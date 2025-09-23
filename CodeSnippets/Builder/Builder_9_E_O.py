class Vehicle:
    def __init__(self): self.parts = []
    def add(self, part): self.parts.append(part)
    def spec(self): return ", ".join(self.parts)

class Assembler:
    def __init__(self): self.reset()
    def reset(self): self._product = Vehicle()
    def add_wheels(self): self._product.add("wheels")
    def add_engine(self): self._product.add("engine")
    def get(self):
        product, self._product = self._product, Vehicle()
        return product

class Coordinator:
    def __init__(self, assembler): self.assembler = assembler
    def construct_minimal(self): self.assembler.add_wheels()
    def construct_full(self): self.assembler.add_wheels(); self.assembler.add_engine()

if __name__ == "__main__":
    assembler = Assembler()
    coordinator = Coordinator(assembler)
    coordinator.construct_minimal()
    v1 = assembler.get()
    coordinator.construct_full()
    v2 = assembler.get()
    print("Minimal:", v1.spec())
    print("Full:", v2.spec())