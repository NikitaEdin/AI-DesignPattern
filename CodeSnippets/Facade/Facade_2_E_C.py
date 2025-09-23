class CPU:
    def start(self):
        print("CPU starting")

class Memory:
    def load(self):
        print("Memory loading")

class HardDrive:
    def read(self):
        print("Hard drive reading")

class Computer:
    def __init__(self):
        self.cpu = CPU()
        self.memory = Memory()
        self.hard_drive = HardDrive()
    
    def start_computer(self):
        self.cpu.start()
        self.memory.load()
        self.hard_drive.read()
        print("Computer ready")

if __name__ == "__main__":
    computer = Computer()
    computer.start_computer()