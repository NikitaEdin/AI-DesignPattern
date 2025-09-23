class SubsystemA:
    def operation1(self): return "A: ready"
    def operation2(self): return "A: processing"
class SubsystemB:
    def task1(self): return "B: initialized"
    def task2(self): return "B: executing"
class SubsystemC:
    def action(self): return "C: finalizing"
class Coordinator:
    def __init__(self):
        self.a = SubsystemA(); self.b = SubsystemB(); self.c = SubsystemC()
    def run(self):
        r = [self.a.operation1(), self.b.task1(), self.a.operation2(), self.b.task2(), self.c.action()]
        return " | ".join(r)
if __name__ == "__main__":
    coordinator = Coordinator()
    print(coordinator.run())