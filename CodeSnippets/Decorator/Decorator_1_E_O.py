class Component:
    def operation(self): raise NotImplementedError
class ConcreteComponent(Component):
    def operation(self): return "Core"
class WrapperBase(Component):
    def __init__(self, component): self._component = component
    def operation(self): return self._component.operation()
class FeatureA(WrapperBase):
    def operation(self): return f"{self._component.operation()} + A"
class FeatureB(WrapperBase):
    def operation(self): return f"{self._component.operation()} + B"
if __name__ == "__main__":
    core = ConcreteComponent()
    wrapped = FeatureA(core)
    wrapped2 = FeatureB(wrapped)
    print(core.operation())
    print(wrapped.operation())
    print(wrapped2.operation())