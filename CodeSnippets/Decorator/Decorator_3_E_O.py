class Component:
    def operation(self) -> str: raise NotImplementedError
class ConcreteComponent(Component):
    def operation(self) -> str: return "Core"
class WrapperBase(Component):
    def __init__(self, component: Component): self._component = component
    def operation(self) -> str: return self._component.operation()
class FancyWrapper(WrapperBase):
    def operation(self) -> str: return f"*{super().operation()}*"
class PrefixWrapper(WrapperBase):
    def operation(self) -> str: return f"-> {super().operation()}"
if __name__ == "__main__":
    core = ConcreteComponent()
    wrapped = FancyWrapper(PrefixWrapper(core))
    print(wrapped.operation())