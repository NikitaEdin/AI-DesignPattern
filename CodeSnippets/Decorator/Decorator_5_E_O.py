from abc import ABC, abstractmethod
class Component(ABC):
    @abstractmethod
    def execute(self): ...
class Core(Component):
    def execute(self):
        return "Core"
class Wrapper(Component):
    def __init__(self, comp):
        self.comp = comp
    def execute(self):
        return self.comp.execute()
class AddFeature(Wrapper):
    def execute(self):
        return "Feature(" + self.comp.execute() + ")"
if __name__ == "__main__":
    core = Core()
    wrapped = AddFeature(core)
    double = AddFeature(wrapped)
    print(core.execute())
    print(wrapped.execute())
    print(double.execute())