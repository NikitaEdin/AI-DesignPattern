class Computer:
    def __init__(self):
        self._cpu = None
        self._ram = None
        self._storage = None
        self._gpu = None
        self._peripherals = []

    def configure(self, cpu, ram, storage, gpu=None, peripherals=None):
        self._cpu = cpu
        self._ram = ram
        self._storage = storage
        if gpu:
            self._gpu = gpu
        if peripherals:
            self._peripherals = peripherals
        return self

    def display_specs(self):
        specs = f"CPU: {self._cpu}, RAM: {self._ram}, Storage: {self._storage}"
        if self._gpu:
            specs += f", GPU: {self._gpu}"
        if self._peripherals:
            specs += f", Peripherals: {', '.join(self._peripherals)}"
        print(specs)

class PcAssembler:
    def __init__(self):
        self.reset()

    def reset(self):
        self._computer = Computer()
        self._cpu = None
        self._ram = None
        self._storage = None
        self._gpu = None
        self._peripherals = []

    def set_cpu(self, cpu):
        self._cpu = cpu
        return self

    def set_ram(self, ram):
        self._ram = ram
        return self

    def set_storage(self, storage):
        self._storage = storage
        return self

    def set_gpu(self, gpu):
        self._gpu = gpu
        return self

    def add_peripheral(self, peripheral):
        self._peripherals.append(peripheral)
        return self

    def assemble(self):
        if not self._cpu or not self._ram or not self._storage:
            raise ValueError("Essential components (CPU, RAM, Storage) must be set.")
        if self._ram < 4:
            raise ValueError("RAM must be at least 4GB.")
        self._computer.configure(
            self._cpu, self._ram, self._storage,
            self._gpu, self._peripherals if self._peripherals else None
        )
        product = self._computer
        self.reset()
        return product

class SystemIntegrator:
    def __init__(self, assembler):
        self._assembler = assembler

    def create_gaming_rig(self):
        return (self._assembler
                .set_cpu("Intel i9")
                .set_ram(16)
                .set_storage("1TB SSD")
                .set_gpu("NVIDIA RTX 3080")
                .add_peripheral("Gaming Mouse")
                .add_peripheral("Mechanical Keyboard")
                .assemble())

    def create_office_setup(self):
        return (self._assembler
                .set_cpu("AMD Ryzen 5")
                .set_ram(8)
                .set_storage("512GB SSD")
                .add_peripheral("Wireless Mouse")
                .add_peripheral("Standard Keyboard")
                .assemble())

    def create_basic_laptop(self):
        try:
            return (self._assembler
                    .set_cpu("Intel i3")
                    .set_ram(4)
                    .set_storage("256GB HDD")
                    .assemble())
        except ValueError as e:
            print(f"Assembly failed: {e}")
            return None

if __name__ == "__main__":
    assembler = PcAssembler()
    integrator = SystemIntegrator(assembler)

    gaming_pc = integrator.create_gaming_rig()
    if gaming_pc:
        print("Gaming Rig:")
        gaming_pc.display_specs()

    office_pc = integrator.create_office_setup()
    if office_pc:
        print("\nOffice Setup:")
        office_pc.display_specs()

    basic_laptop = integrator.create_basic_laptop()
    if basic_laptop:
        print("\nBasic Laptop:")
        basic_laptop.display_specs()