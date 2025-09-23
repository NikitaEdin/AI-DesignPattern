class CPU:
    def freeze(self):
        print("CPU: freeze")
    def jump(self, position):
        print(f"CPU: jump to {position}")
    def execute(self):
        print("CPU: execute")

class Memory:
    def load(self, position, data):
        print(f"Memory: load {data} at {position}")

class Disk:
    def read(self, lba, size):
        return f"boot_sector_data_from_{lba}_size_{size}"

class ComputerSystem:
    def __init__(self):
        self.cpu = CPU()
        self.memory = Memory()
        self.disk = Disk()
    def start(self):
        self.cpu.freeze()
        data = self.disk.read(0, 512)
        self.memory.load(0, data)
        self.cpu.jump(0)
        self.cpu.execute()

if __name__ == "__main__":
    system = ComputerSystem()
    system.start()