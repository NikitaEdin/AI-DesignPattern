import abc
class Action(abc.ABC):
    @abc.abstractmethod
    def do(self, a, b): pass
class AddAction(Action):
    def do(self, a, b): return a + b
class MultiplyAction(Action):
    def do(self, a, b): return a * b
class Worker:
    def __init__(self, action: Action): self.action = action
    def set_action(self, action: Action): self.action = action
    def run(self, a, b): return self.action.do(a, b)
if __name__ == "__main__":
    worker = Worker(AddAction())
    print("add:", worker.run(3, 4))
    worker.set_action(MultiplyAction())
    print("mul:", worker.run(3, 4))