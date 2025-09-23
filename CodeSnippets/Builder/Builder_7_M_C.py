class Computer:
    def __init__(self):
        self.cpu = None
        self.memory = None
        self.storage = None
        self.graphics = None
        self.operating_system = None

    def __str__(self):
        return f"Computer(CPU: {self.cpu}, Memory: {self.memory}GB, Storage: {self.storage}GB, Graphics: {self.graphics}, OS: {self.operating_system})"

class ComputerAssembler:
    def __init__(self):
        self.reset()

    def reset(self):
        self._computer = Computer()
        return self

    def add_cpu(self, cpu):
        if not cpu:
            raise ValueError("CPU cannot be empty")
        self._computer.cpu = cpu
        return self

    def add_memory(self, memory):
        if memory <= 0:
            raise ValueError("Memory must be positive")
        self._computer.memory = memory
        return self

    def add_storage(self, storage):
        if storage <= 0:
            raise ValueError("Storage must be positive")
        self._computer.storage = storage
        return self

    def add_graphics(self, graphics):
        self._computer.graphics = graphics
        return self

    def install_os(self, os):
        self._computer.operating_system = os
        return self

    def build(self):
        if not all([self._computer.cpu, self._computer.memory, self._computer.storage]):
            raise ValueError("CPU, memory, and storage are required")
        result = self._computer
        self.reset()
        return result

if __name__ == "__main__":
    assembler = ComputerAssembler()
    
    gaming_pc = (assembler
                 .add_cpu("Intel i7-12700K")
                 .add_memory(32)
                 .add_storage(1000)
                 .add_graphics("RTX 4070")
                 .install_os("Windows 11")
                 .build())
    
    office_pc = (assembler
                 .add_cpu("AMD Ryzen 5")
                 .add_memory(16)
                 .add_storage(512)
                 .install_os("Ubuntu")
                 .build())
    
    print(gaming_pc)
    print(office_pc)