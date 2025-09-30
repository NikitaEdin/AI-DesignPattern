class CPU:
    def freeze(self): pass
    def jump(self, position): pass
    def execute(self): pass

class Memory:
    def load(self, position, data): pass

class Drive:
    def read(self, lba, size): return []

class Computer:
    def __init__(self):
        self.cpu = CPU()
        self.memory = Memory()
        self.drive = Drive()
    def boot(self):
        self.cpu.freeze()
        self.memory.load(0, self.drive.read(0, 1024))
        self.cpu.jump(0)
        self.cpu.execute()

if __name__ == "__main__":
    pc = Computer()
    pc.boot()