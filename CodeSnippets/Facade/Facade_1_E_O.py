class SubsystemA:
    def __init__(self, name): self.name = name
    def prepare(self): return f"{self.name} prepared"
    def run(self): return f"{self.name} running"

class SubsystemB:
    def __init__(self, number): self.number = number
    def configure(self): return f"configured {self.number}"
    def execute(self): return f"executed {self.number}"

class Coordinator:
    def __init__(self, a=None, b=None):
        self.a = a or SubsystemA("A1")
        self.b = b or SubsystemB(42)
    def perform_task(self):
        steps = [self.a.prepare(), self.b.configure(), self.a.run(), self.b.execute()]
        return " | ".join(steps)

if __name__ == "__main__":
    c = Coordinator()
    print(c.perform_task())