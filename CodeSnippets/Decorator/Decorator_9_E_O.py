class Component:
    def operation(self) -> str:
        raise NotImplementedError

class ConcreteComponent(Component):
    def operation(self) -> str:
        return "Core"

class WrapperBase(Component):
    def __init__(self, component: Component):
        self._component = component
    def operation(self) -> str:
        return self._component.operation()

class PrefixWrapper(WrapperBase):
    def operation(self) -> str:
        return "[PRE]" + super().operation()

class SuffixWrapper(WrapperBase):
    def operation(self) -> str:
        return super().operation() + "[POST]"

if __name__ == "__main__":
    core = ConcreteComponent()
    wrapped_once = PrefixWrapper(core)
    wrapped_twice = SuffixWrapper(wrapped_once)
    print(core.operation())
    print(wrapped_once.operation())
    print(wrapped_twice.operation())