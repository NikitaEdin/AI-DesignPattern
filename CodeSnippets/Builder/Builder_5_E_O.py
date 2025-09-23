class Product:
    def __init__(self):
        self.parts = []
    def add(self, part):
        self.parts.append(part)
    def __str__(self):
        return "Product: " + ", ".join(self.parts)

class AssemblerBase:
    def reset(self): raise NotImplementedError
    def assemble_one(self): raise NotImplementedError
    def assemble_two(self): raise NotImplementedError
    def retrieve(self): raise NotImplementedError

class ConcreteAssembler(AssemblerBase):
    def reset(self):
        self.product = Product()
    def assemble_one(self):
        self.product.add("Part A")
    def assemble_two(self):
        self.product.add("Part B")
    def retrieve(self):
        p = self.product
        self.reset()
        return p

class Coordinator:
    def __init__(self, assembler):
        self.assembler = assembler
    def minimal(self):
        self.assembler.reset()
        self.assembler.assemble_one()
        return self.assembler.retrieve()
    def full(self):
        self.assembler.reset()
        self.assembler.assemble_one()
        self.assembler.assemble_two()
        return self.assembler.retrieve()

if __name__ == "__main__":
    asm = ConcreteAssembler()
    director = Coordinator(asm)
    print(director.minimal())
    print(director.full())