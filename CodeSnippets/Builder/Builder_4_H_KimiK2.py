from typing import Optional, List
import time

class CustomComputer:
    def __init__(self):
        self.cpu: Optional[str] = None
        self.gpu: Optional[str] = None
        self.ram: int = 0
        self.storage: int = 0
        self.cooling: Optional[str] = None
        self.led_color: Optional[str] = None
        self.timestamp: float = time.time()

    def __str__(self):
        return (f"Computer(cpu={self.cpu}, gpu={self.gpu}, ram={self.ram}GB, "
                f"storage={self.storage}GB, cooling={self.cooling}, led={self.led_color})")

class ComputerAssembler:
    def __init__(self):
        self.computer = CustomComputer()

    def reset(self):
        self.computer = CustomComputer()
        return self

    def set_cpu(self, cpu: str):
        self.computer.cpu = cpu
        return self

    def set_gpu(self, gpu: str):
        self.computer.gpu = gpu
        return self

    def set_ram(self, ram: int):
        if ram <= 0:
            raise ValueError("RAM must be positive")
        self.computer.ram = ram
        return self

    def set_storage(self, storage: int):
        if storage <= 0:
            raise ValueError("Storage must be positive")
        self.computer.storage = storage
        return self

    def set_cooling(self, cooling: str):
        self.computer.cooling = cooling
        return self

    def set_led_color(self, color: str):
        self.computer.led_color = color
        return self

    def assemble(self) -> CustomComputer:
        if not self.computer.cpu or not self.computer.gpu:
            raise ValueError("CPU and GPU are required")
        result = self.computer
        self.reset()
        return result

class Director:
    def __init__(self, assembler: ComputerAssembler):
        self.assembler = assembler

    def create_gaming_rig(self):
        return (self.assembler
                .set_cpu("Intel i9")
                .set_gpu("RTX 4090")
                .set_ram(32)
                .set_storage(2000)
                .set_cooling("Liquid")
                .set_led_color("RGB")
                .assemble())

    def create_office_pc(self):
        return (self.assembler
                .set_cpu("Intel i5")
                .set_gpu("Integrated")
                .set_ram(16)
                .set_storage(500)
                .assemble())

if __name__ == "__main__":
    assembler = ComputerAssembler()
    director = Director(assembler)

    gaming = director.create_gaming_rig()
    office = director.create_office_pc()

    print(gaming)
    print(office)

    custom = (assembler
              .set_cpu("AMD Ryzen 7")
              .set_gpu("RX 7800 XT")
              .set_ram(64)
              .set_storage(4000)
              .set_led_color("Red")
              .assemble())
    print(custom)