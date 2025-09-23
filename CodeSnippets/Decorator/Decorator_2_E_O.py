class Component:
    def operation(self): raise NotImplementedError
class ConcreteComponent(Component):
    def operation(self): return "Base"
class WrapperBase(Component):
    def __init__(self, comp): self._comp = comp
    def operation(self): return self._comp.operation()
class FancyWrapper(WrapperBase):
    def operation(self): return f"{self._comp.operation()} + Fancy"
class BoldWrapper(WrapperBase):
    def operation(self): return f"**{self._comp.operation()}**"
if __name__ == "__main__":
    base = ConcreteComponent()
    wrapped = FancyWrapper(BoldWrapper(base))
    print(base.operation())
    print(wrapped.operation())