class Component:
    def operation(self):
        raise NotImplementedError

class SimpleMessage(Component):
    def __init__(self, text):
        self.text = text
    def operation(self):
        return self.text

class Wrapper(Component):
    def __init__(self, component):
        self._component = component
    def operation(self):
        return self._component.operation()

class StarWrapper(Wrapper):
    def operation(self):
        return "***" + super().operation() + "***"

class BracketWrapper(Wrapper):
    def operation(self):
        return "[" + super().operation() + "]"

if __name__ == "__main__":
    base = SimpleMessage("Hello")
    wrapped = StarWrapper(BracketWrapper(base))
    print(wrapped.operation())