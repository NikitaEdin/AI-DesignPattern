class Computer:
    def __init__(self, cpu, ram_gb, storage_gb, gpu=None, operating_system=None):
        self.cpu = cpu
        self.ram_gb = ram_gb
        self.storage_gb = storage_gb
        self.gpu = gpu
        self.operating_system = operating_system

    def __str__(self):
        gpu_str = f", gpu={self.gpu}" if self.gpu else ""
        os_str = f", os={self.operating_system}" if self.operating_system else ""
        return f"Computer(cpu={self.cpu}, ram={self.ram_gb}GB, storage={self.storage_gb}GB{gpu_str}{os_str})"

class SystemConfigurator:
    def __init__(self):
        self.reset()

    def reset(self):
        self._cpu = None
        self._ram_gb = None
        self._storage_gb = None
        self._gpu = None
        self._operating_system = None

    def with_cpu(self, cpu):
        if not isinstance(cpu, str) or len(cpu.strip()) < 3:
            raise ValueError("CPU specification must be a non-empty string of at least 3 characters")
        self._cpu = cpu.strip()
        return self

    def with_ram(self, ram_gb):
        if not isinstance(ram_gb, int) or ram_gb < 4 or ram_gb > 128:
            raise ValueError("RAM must be an integer between 4 and 128 GB inclusive")
        self._ram_gb = ram_gb
        return self

    def with_storage(self, storage_gb):
        if not isinstance(storage_gb, int) or storage_gb < 64:
            raise ValueError("Storage must be at least 64 GB")
        self._storage_gb = storage_gb
        return self

    def with_gpu(self, gpu):
        if gpu is not None and not isinstance(gpu, str):
            raise ValueError("GPU specification must be a string or None")
        self._gpu = gpu
        return self

    def with_operating_system(self, os):
        if os is not None and not isinstance(os, str):
            raise ValueError("Operating system must be a string or None")
        # Edge case: basic compatibility check
        if self._cpu and "AMD" in self._cpu and os == "macOS":
            raise ValueError("macOS is not compatible with AMD CPUs")
        self._operating_system = os
        return self

    def assemble(self):
        if self._cpu is None:
            raise ValueError("CPU is required")
        if self._ram_gb is None:
            raise ValueError("RAM is required")
        if self._storage_gb is None:
            raise ValueError("Storage is required")
        # Additional edge case: ensure sufficient storage for OS if specified
        if self._operating_system and self._storage_gb < 100:
            raise ValueError("At least 100 GB storage required when OS is specified")
        return Computer(
            self._cpu,
            self._ram_gb,
            self._storage_gb,
            self._gpu,
            self._operating_system
        )

if __name__ == "__main__":
    configurator = SystemConfigurator()
    try:
        computer = (configurator
                    .with_cpu("Intel Core i7-12700K")
                    .with_ram(32)
                    .with_storage(1024)
                    .with_gpu("NVIDIA RTX 3080")
                    .with_operating_system("Windows 11")
                    .assemble())
        print(str(computer))
    except ValueError as e:
        print(f"Configuration error: {e}")

    configurator.reset()
    try:
        invalid_computer = (configurator
                            .with_cpu("AMD Ryzen 5")
                            .with_ram(8)
                            .with_storage(128)
                            .with_operating_system("macOS")
                            .assemble())
    except ValueError as e:
        print(f"Compatibility error: {e}")

    configurator.reset()
    try:
        low_ram = configurator.with_ram(2).assemble()
    except ValueError as e:
        print(f"Validation error: {e}")