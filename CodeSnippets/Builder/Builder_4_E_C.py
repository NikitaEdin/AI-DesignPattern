class Computer:
    def __init__(self):
        self.cpu = None
        self.ram = None
        self.storage = None
    
    def __str__(self):
        return f"CPU: {self.cpu}, RAM: {self.ram}, Storage: {self.storage}"

class ComputerAssembler:
    def __init__(self):
        self.computer = Computer()
    
    def set_cpu(self, cpu):
        self.computer.cpu = cpu
        return self
    
    def set_ram(self, ram):
        self.computer.ram = ram
        return self
    
    def set_storage(self, storage):
        self.computer.storage = storage
        return self
    
    def build(self):
        return self.computer

if __name__ == "__main__":
    assembler = ComputerAssembler()
    computer = assembler.set_cpu("Intel i7").set_ram("16GB").set_storage("1TB SSD").build()
    print(computer)