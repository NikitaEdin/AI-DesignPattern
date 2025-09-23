class Component:
    def operation(self):
        return "Base"

class Wrapper:
    def __init__(self, component):
        self._component = component
    
    def operation(self):
        return self._component.operation()

class ConcreteWrapper(Wrapper):
    def operation(self):
        return f"Enhanced({super().operation()})"

class AnotherWrapper(Wrapper):
    def operation(self):
        return f"Modified({super().operation()})"

if __name__ == "__main__":
    base = Component()
    print(base.operation())
    
    wrapped = ConcreteWrapper(base)
    print(wrapped.operation())
    
    double_wrapped = AnotherWrapper(wrapped)
    print(double_wrapped.operation())