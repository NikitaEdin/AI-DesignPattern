class Computer:
    def __init__(self):
        self.cpu = None
        self.ram = None
        self.storage = None
        self.gpu = None
        self.os = None
    
    def __str__(self):
        return f"Computer(CPU: {self.cpu}, RAM: {self.ram}GB, Storage: {self.storage}GB, GPU: {self.gpu}, OS: {self.os})"

class ComputerAssembler:
    def __init__(self):
        self.computer = Computer()
    
    def add_cpu(self, cpu):
        if not cpu:
            raise ValueError("CPU cannot be empty")
        self.computer.cpu = cpu
        return self
    
    def add_ram(self, ram):
        if ram <= 0:
            raise ValueError("RAM must be positive")
        self.computer.ram = ram
        return self
    
    def add_storage(self, storage):
        if storage <= 0:
            raise ValueError("Storage must be positive")
        self.computer.storage = storage
        return self
    
    def add_gpu(self, gpu):
        self.computer.gpu = gpu
        return self
    
    def add_os(self, os):
        self.computer.os = os
        return self
    
    def build(self):
        if not self.computer.cpu or not self.computer.ram:
            raise ValueError("CPU and RAM are required")
        return self.computer

class ComputerDirector:
    @staticmethod
    def create_gaming_pc():
        return (ComputerAssembler()
                .add_cpu("Intel i7")
                .add_ram(32)
                .add_storage(1000)
                .add_gpu("RTX 4080")
                .add_os("Windows 11")
                .build())

if __name__ == "__main__":
    gaming_pc = ComputerDirector.create_gaming_pc()
    print(gaming_pc)
    
    custom_pc = (ComputerAssembler()
                 .add_cpu("AMD Ryzen 7")
                 .add_ram(16)
                 .add_storage(500)
                 .build())
    print(custom_pc)