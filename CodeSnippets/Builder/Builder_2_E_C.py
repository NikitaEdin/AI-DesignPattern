class Computer:
    def __init__(self):
        self.cpu = None
        self.memory = None
        self.storage = None
    
    def __str__(self):
        return f"CPU: {self.cpu}, Memory: {self.memory}, Storage: {self.storage}"

class ComputerAssembler:
    def __init__(self):
        self.computer = Computer()
    
    def add_cpu(self, cpu):
        self.computer.cpu = cpu
        return self
    
    def add_memory(self, memory):
        self.computer.memory = memory
        return self
    
    def add_storage(self, storage):
        self.computer.storage = storage
        return self
    
    def get_computer(self):
        return self.computer

if __name__ == "__main__":
    assembler = ComputerAssembler()
    computer = assembler.add_cpu("Intel i7").add_memory("16GB").add_storage("1TB SSD").get_computer()
    print(computer)