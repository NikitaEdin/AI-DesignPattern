class Computer:
    def __init__(self, processor=None, memory=None, storage=None, gpu=None):
        self.processor = processor
        self.memory = memory
        self.storage = storage
        self.gpu = gpu

    def display_specs(self):
        specs = f"Processor: {self.processor}\nMemory: {self.memory}\nStorage: {self.storage}"
        if self.gpu:
            specs += f"\nGPU: {self.gpu}"
        return specs

class ComputerConfigurator:
    def __init__(self):
        self._processor = None
        self._memory = None
        self._storage = None
        self._gpu = None

    def set_processor(self, processor):
        self._processor = processor
        return self

    def set_memory(self, memory):
        self._memory = memory
        return self

    def set_storage(self, storage):
        self._storage = storage
        return self

    def set_gpu(self, gpu):
        self._gpu = gpu
        return self

    def create(self):
        if not self._processor:
            raise ValueError("Processor is required for computer configuration.")
        return Computer(self._processor, self._memory, self._storage, self._gpu)

if __name__ == "__main__":
    try:
        config = (ComputerConfigurator()
                  .set_processor("Intel Core i7")
                  .set_memory("16GB RAM")
                  .set_storage("1TB SSD")
                  .set_gpu("NVIDIA RTX 3080"))
        computer = config.create()
        print(computer.display_specs())
    except ValueError as e:
        print(f"Error: {e}")