class CPU:
    def start(self):
        print("CPU starting")

class Memory:
    def load(self):
        print("Memory loading")

class HardDrive:
    def read(self):
        print("HardDrive reading")

class Computer:
    def __init__(self):
        self.cpu = CPU()
        self.memory = Memory()
        self.hd = HardDrive()

    def start(self):
        self.cpu.start()
        self.memory.load()
        self.hd.read()
        print("Computer started")

if __name__ == "__main__":
    comp = Computer()
    comp.start()