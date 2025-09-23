class Laptop:
    def __init__(self):
        self.cpu = None
        self.ram = None
        self.storage = None
        self.graphics = None
        self.screen_size = None

    def __str__(self):
        return (f"Laptop: CPU={self.cpu}, RAM={self.ram}GB, "
                f"Storage={self.storage}GB, Graphics={self.graphics}, "
                f"Screen={self.screen_size}in")

class LaptopConfigurer:
    def __init__(self):
        self._laptop = Laptop()
        self._required_parts = {'cpu', 'ram', 'storage'}

    def with_cpu(self, cpu):
        self._laptop.cpu = cpu
        self._required_parts.discard('cpu')
        return self

    def with_ram(self, ram_gb):
        if ram_gb <= 0:
            raise ValueError("RAM must be positive")
        self._laptop.ram = ram_gb
        self._required_parts.discard('ram')
        return self

    def with_storage(self, storage_gb):
        if storage_gb <= 0:
            raise ValueError("Storage must be positive")
        self._laptop.storage = storage_gb
        self._required_parts.discard('storage')
        return self

    def with_graphics(self, graphics):
        self._laptop.graphics = graphics
        return self

    def with_screen_size(self, size_in):
        if size_in < 10 or size_in > 20:
            raise ValueError("Screen size must be between 10 and 20 inches")
        self._laptop.screen_size = size_in
        return self

    def create(self):
        if self._required_parts:
            missing = ', '.join(self._required_parts)
            raise ValueError(f"Missing required parts: {missing}")
        return self._laptop

class GamingLaptopConfigurer(LaptopConfigurer):
    def __init__(self):
        super().__init__()
        self.with_cpu("High-end Intel i9").with_ram(32).with_storage(1000).with_graphics("NVIDIA RTX 4080")

class BusinessLaptopConfigurer(LaptopConfigurer):
    def __init__(self):
        super().__init__()
        self.with_cpu("Intel i7").with_ram(16).with_storage(512).with_graphics("Integrated")

class LaptopAssembler:
    def __init__(self, configurer):
        self._configurer = configurer

    def assemble_gaming(self):
        self._configurer.with_graphics("NVIDIA RTX 4080").with_screen_size(17)
        return self._configurer.create()

    def assemble_business(self):
        self._configurer.with_graphics("Integrated").with_screen_size(14)
        return self._configurer.create()

    def assemble_custom(self):
        return self._configurer.create()

if __name__ == "__main__":
    gaming_config = GamingLaptopConfigurer()
    assembler = LaptopAssembler(gaming_config)
    gaming_laptop = assembler.assemble_gaming()
    print(gaming_laptop)

    business_config = BusinessLaptopConfigurer()
    assembler = LaptopAssembler(business_config)
    business_laptop = assembler.assemble_business()
    print(business_laptop)

    try:
        custom_config = LaptopConfigurer()
        custom_laptop = custom_config.with_cpu("AMD Ryzen 7").with_ram(16).create()
        print(custom_laptop)
    except ValueError as e:
        print(f"Error: {e}")