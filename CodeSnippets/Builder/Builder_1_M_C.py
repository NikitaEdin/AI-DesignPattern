class Computer:
    def __init__(self):
        self.cpu = None
        self.ram = None
        self.storage = None
        self.graphics = None
        self.os = None
    
    def __str__(self):
        return f"Computer(CPU: {self.cpu}, RAM: {self.ram}GB, Storage: {self.storage}GB, Graphics: {self.graphics}, OS: {self.os})"

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
    
    def set_ram(self, ram):
        if ram <= 0:
            raise ValueError("RAM must be positive")
        self.computer.ram = ram
        return self
    
    def set_storage(self, storage):
        if storage <= 0:
            raise ValueError("Storage must be positive")
        self.computer.storage = storage
        return self
    
    def set_graphics(self, graphics):
        self.computer.graphics = graphics
        return self
    
    def set_os(self, os):
        self.computer.os = os
        return self
    
    def build(self):
        if not all([self.computer.cpu, self.computer.ram, self.computer.storage]):
            raise ValueError("CPU, RAM, and Storage are required")
        result = self.computer
        self.reset()
        return result

if __name__ == "__main__":
    assembler = ComputerAssembler()
    
    gaming_pc = (assembler
                 .set_cpu("Intel i7")
                 .set_ram(32)
                 .set_storage(1000)
                 .set_graphics("RTX 4080")
                 .set_os("Windows 11")
                 .build())
    
    office_pc = (assembler
                 .set_cpu("Intel i5")
                 .set_ram(16)
                 .set_storage(500)
                 .set_os("Ubuntu")
                 .build())
    
    print(gaming_pc)
    print(office_pc)