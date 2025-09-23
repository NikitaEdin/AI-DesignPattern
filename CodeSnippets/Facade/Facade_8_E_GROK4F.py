class Cpu:
    def start(self):
        print("CPU starts")

class Ram:
    def load(self):
        print("RAM loads program")

class Disk:
    def read(self):
        print("Disk reads data")

class System:
    def __init__(self):
        self.cpu = Cpu()
        self.ram = Ram()
        self.disk = Disk()

    def boot(self):
        self.cpu.start()
        self.disk.read()
        self.ram.load()
        print("System booted")

if __name__ == "__main__":
    computer = System()
    computer.boot()