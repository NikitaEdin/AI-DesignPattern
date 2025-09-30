class Computer:
    def __init__(self):
        self.cpu = None
        self.memory = None
        self.storage = None
        self.graphics = None
    
    def __str__(self):
        return f"Computer: {self.cpu}, {self.memory}GB RAM, {self.storage}GB SSD, {self.graphics}"

class Configurator:
    def __init__(self):
        self.computer = Computer()
    
    def add_cpu(self, cpu):
        if not cpu:
            raise ValueError("CPU cannot be empty")
        self.computer.cpu = cpu
        return self
    
    def add_memory(self, memory):
        if memory <= 0:
            raise ValueError("Memory must be positive")
        self.computer.memory = memory
        return self
    
    def add_storage(self, storage):
        if storage <= 0:
            raise ValueError("Storage must be positive")
        self.computer.storage = storage
        return self
    
    def add_graphics(self, graphics):
        self.computer.graphics = graphics
        return self
    
    def build(self):
        if not self.computer.cpu or not self.computer.memory:
            raise ValueError("CPU and memory are required")
        return self.computer

if __name__ == "__main__":
    gaming_pc = Configurator() \
        .add_cpu("Intel i9") \
        .add_memory(32) \
        .add_storage(1000) \
        .add_graphics("RTX 4080") \
        .build()
    
    office_pc = Configurator() \
        .add_cpu("AMD Ryzen 5") \
        .add_memory(16) \
        .add_storage(512) \
        .build()
    
    print(gaming_pc)
    print(office_pc)