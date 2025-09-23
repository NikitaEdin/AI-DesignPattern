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
        return f"Enhanced({self._component.operation()})"

class AnotherWrapper(Wrapper):
    def operation(self):
        return f"Modified[{self._component.operation()}]"

if __name__ == "__main__":
    base = Component()
    print(base.operation())
    
    enhanced = ConcreteWrapper(base)
    print(enhanced.operation())
    
    double_wrapped = AnotherWrapper(enhanced)
    print(double_wrapped.operation())