class Computer:
    def __init__(self):
        self.cpu = None
        self.memory = None
        self.storage = None
        self.graphics = None
        self.case = None
    
    def __str__(self):
        return f"Computer: CPU={self.cpu}, Memory={self.memory}GB, Storage={self.storage}, Graphics={self.graphics}, Case={self.case}"

class ComputerAssembler:
    def __init__(self):
        self.reset()
    
    def reset(self):
        self._computer = Computer()
        return self
    
    def set_cpu(self, cpu):
        if not cpu:
            raise ValueError("CPU cannot be empty")
        self._computer.cpu = cpu
        return self
    
    def set_memory(self, memory):
        if memory <= 0:
            raise ValueError("Memory must be positive")
        self._computer.memory = memory
        return self
    
    def set_storage(self, storage):
        self._computer.storage = storage
        return self
    
    def set_graphics(self, graphics):
        self._computer.graphics = graphics
        return self
    
    def set_case(self, case):
        self._computer.case = case
        return self
    
    def build(self):
        if not self._computer.cpu or not self._computer.memory:
            raise ValueError("CPU and memory are required")
        result = self._computer
        self.reset()
        return result

class ComputerDirector:
    def __init__(self, assembler):
        self._assembler = assembler
    
    def create_gaming_computer(self):
        return (self._assembler
                .set_cpu("Intel i9")
                .set_memory(32)
                .set_storage("1TB SSD")
                .set_graphics("RTX 4080")
                .set_case("RGB Tower")
                .build())
    
    def create_office_computer(self):
        return (self._assembler
                .set_cpu("Intel i5")
                .set_memory(16)
                .set_storage("512GB SSD")
                .set_graphics("Integrated")
                .set_case("Compact")
                .build())

if __name__ == "__main__":
    assembler = ComputerAssembler()
    director = ComputerDirector(assembler)
    
    gaming_pc = director.create_gaming_computer()
    print(gaming_pc)
    
    office_pc = director.create_office_computer()
    print(office_pc)
    
    custom_pc = (assembler
                 .set_cpu("AMD Ryzen 7")
                 .set_memory(16)
                 .set_storage("256GB SSD")
                 .build())
    print(custom_pc)