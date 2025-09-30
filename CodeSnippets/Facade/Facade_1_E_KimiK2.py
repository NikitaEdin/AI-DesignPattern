class Cpu:
    def execute(self): return "executing"

class Memory:
    def load(self): return "loading"

class Disk:
    def read(self): return "reading"

class Computer:
    def __init__(self):
        self.cpu = Cpu()
        self.ram = Memory()
        self.disk = Disk()
    def run(self):
        return "start "+self.disk.read()+" "+self.ram.load()+" "+self.cpu.execute()
if __name__=='__main__':
    pc=Computer()
    print(pc.run())