from dataclasses import dataclass
from typing import Optional

@dataclass
class Computer:
    cpu: str
    gpu: str
    ram: int
    storage: int
    cooling: Optional[str] = None

class TechAssembler:
    def __init__(self) -> None:
        self._computer = Computer(cpu="", gpu="", ram=0, storage=0)

    def add_processor(self, model: str) -> "TechAssembler":
        self._computer.cpu = model
        return self

    def add_graphics(self, model: str) -> "TechAssembler":
        self._computer.gpu = model
        return self

    def add_memory(self, size: int) -> "TechAssembler":
        if size <= 0:
            raise ValueError("Memory must be positive")
        self._computer.ram = size
        return self

    def add_storage(self, size: int) -> "TechAssembler":
        if size <= 0:
            raise ValueError("Storage must be positive")
        self._computer.storage = size
        return self

    def add_cooling(self, system: str) -> "TechAssembler":
        self._computer.cooling = system
        return self

    def finalize(self) -> Computer:
        if not self._computer.cpu or not self._computer.gpu:
            raise ValueError("Missing essential components")
        return self._computer

if __name__ == "__main__":
    gaming_pc = (TechAssembler()
                 .add_processor("Intel i9")
                 .add_graphics("RTX 4090")
                 .add_memory(32)
                 .add_storage(1000)
                 .add_cooling("Liquid")
                 .finalize())
    
    print(gaming_pc)