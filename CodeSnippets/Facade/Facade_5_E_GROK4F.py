class Processor:
    def start(self):
        print("Processor starting")

class Ram:
    def load(self):
        print("RAM loading")

class Disk:
    def initialize(self):
        print("Disk initializing")

class Computer:
    def __init__(self):
        self.processor = Processor()
        self.ram = Ram()
        self.disk = Disk()

    def boot(self):
        self.disk.initialize()
        self.ram.load()
        self.processor.start()
        print("System booted")

if __name__ == "__main__":
    system = Computer()
    system.boot()