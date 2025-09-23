class Computer:
    def __init__(self):
        self.cpu = None
        self.memory = None
        self.storage = None
        self.graphics = None
        self.os = None
    
    def __str__(self):
        return f"Computer: CPU={self.cpu}, RAM={self.memory}GB, Storage={self.storage}, GPU={self.graphics}, OS={self.os}"

class SystemAssembler:
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.computer = Computer()
        return self
    
    def add_processor(self, cpu):
        if not cpu:
            raise ValueError("CPU cannot be empty")
        self.computer.cpu = cpu
        return self
    
    def add_memory(self, memory_gb):
        if memory_gb <= 0:
            raise ValueError("Memory must be positive")
        self.computer.memory = memory_gb
        return self
    
    def add_storage(self, storage):
        if not storage:
            raise ValueError("Storage cannot be empty")
        self.computer.storage = storage
        return self
    
    def add_graphics(self, gpu):
        self.computer.graphics = gpu
        return self
    
    def install_os(self, operating_system):
        self.computer.os = operating_system
        return self
    
    def build(self):
        if not all([self.computer.cpu, self.computer.memory, self.computer.storage]):
            raise ValueError("Missing required components")
        result = self.computer
        self.reset()
        return result

if __name__ == "__main__":
    assembler = SystemAssembler()
    
    gaming_pc = (assembler
                .add_processor("Intel i7-13700K")
                .add_memory(32)
                .add_storage("1TB NVMe SSD")
                .add_graphics("RTX 4080")
                .install_os("Windows 11")
                .build())
    
    office_pc = (assembler
                .add_processor("AMD Ryzen 5")
                .add_memory(16)
                .add_storage("512GB SSD")
                .install_os("Ubuntu")
                .build())
    
    print(gaming_pc)
    print(office_pc)