class Computer:
    def __init__(self):
        self.cpu = None
        self.memory = None
        self.storage = None
        self.graphics = None
        self.operating_system = None
    
    def __str__(self):
        return f"Computer: CPU={self.cpu}, Memory={self.memory}GB, Storage={self.storage}GB, Graphics={self.graphics}, OS={self.operating_system}"

class ComputerAssembler:
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.computer = Computer()
        return self
    
    def set_cpu(self, cpu):
        if not cpu:
            raise ValueError("CPU cannot be empty")
        self.computer.cpu = cpu
        return self
    
    def set_memory(self, memory):
        if memory <= 0:
            raise ValueError("Memory must be positive")
        self.computer.memory = memory
        return self
    
    def set_storage(self, storage):
        if storage <= 0:
            raise ValueError("Storage must be positive")
        self.computer.storage = storage
        return self
    
    def set_graphics(self, graphics):
        self.computer.graphics = graphics
        return self
    
    def set_operating_system(self, os):
        self.computer.operating_system = os
        return self
    
    def build(self):
        if not all([self.computer.cpu, self.computer.memory, self.computer.storage]):
            raise ValueError("CPU, memory, and storage are required")
        result = self.computer
        self.reset()
        return result

if __name__ == "__main__":
    assembler = ComputerAssembler()
    
    gaming_pc = (assembler
                 .set_cpu("Intel i9")
                 .set_memory(32)
                 .set_storage(1000)
                 .set_graphics("RTX 4080")
                 .set_operating_system("Windows 11")
                 .build())
    
    office_pc = (assembler
                 .set_cpu("Intel i5")
                 .set_memory(16)
                 .set_storage(500)
                 .set_operating_system("Ubuntu")
                 .build())
    
    print(gaming_pc)
    print(office_pc)