import abc

class Computer:
    def __init__(self):
        self.cpu = None
        self.gpu = None
        self.ram = None
        self.storage = None

    def __repr__(self):
        parts = [
            f"CPU={self.cpu or 'N/A'}",
            f"GPU={self.gpu or 'N/A'}",
            f"RAM={self.ram or 'N/A'}",
            f"Storage={self.storage or 'N/A'}",
        ]
        return f"Computer({', '.join(parts)})"

class AssemblerInterface(abc.ABC):
    @abc.abstractmethod
    def set_cpu(self, cpu): ...
    @abc.abstractmethod
    def set_gpu(self, gpu): ...
    @abc.abstractmethod
    def set_ram(self, ram): ...
    @abc.abstractmethod
    def set_storage(self, storage): ...
    @abc.abstractmethod
    def retrieve_product(self): ...
    @abc.abstractmethod
    def reset(self): ...

class GamingAssembler(AssemblerInterface):
    def __init__(self):
        self.reset()

    def set_cpu(self, cpu):
        self._product.cpu = cpu
        return self

    def set_gpu(self, gpu):
        self._product.gpu = gpu
        return self

    def set_ram(self, ram):
        self._product.ram = ram
        return self

    def set_storage(self, storage):
        self._product.storage = storage
        return self

    def retrieve_product(self):
        if not self._product.cpu or not self._product.ram:
            raise ValueError("Incomplete configuration: CPU and RAM are required")
        product = self._product
        self.reset()
        return product

    def reset(self):
        self._product = Computer()

class OfficeAssembler(AssemblerInterface):
    def __init__(self):
        self.reset()

    def set_cpu(self, cpu):
        self._product.cpu = cpu
        return self

    def set_gpu(self, gpu):
        self._product.gpu = gpu
        return self

    def set_ram(self, ram):
        self._product.ram = ram
        return self

    def set_storage(self, storage):
        self._product.storage = storage
        return self

    def retrieve_product(self):
        if not self._product.cpu or not self._product.ram:
            raise ValueError("Incomplete configuration: CPU and RAM are required")
        product = self._product
        self.reset()
        return product

    def reset(self):
        self._product = Computer()

class AssemblyCoordinator:
    def assemble_high_performance(self, assembler: AssemblerInterface):
        assembler.set_cpu("Intel i9").set_gpu("NVIDIA RTX 4090").set_ram("32GB").set_storage("2TB NVMe")

    def assemble_budget_office(self, assembler: AssemblerInterface):
        assembler.set_cpu("Intel i5").set_ram("8GB").set_storage("256GB SSD")

if __name__ == "__main__":
    coordinator = AssemblyCoordinator()
    ga = GamingAssembler()
    coordinator.assemble_high_performance(ga)
    gaming_pc = ga.retrieve_product()
    print("Assembled high-performance:", gaming_pc)

    oa = OfficeAssembler()
    coordinator.assemble_budget_office(oa)
    office_pc = oa.retrieve_product()
    print("Assembled office machine:", office_pc)

    incomplete = OfficeAssembler()
    incomplete.set_cpu("AMD Ryzen 3")
    try:
        incomplete.retrieve_product()
    except ValueError as e:
        print("Error during assembly:", e)