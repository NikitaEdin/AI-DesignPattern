class Component:
    def operation(self):
        return "Base"

class Wrapper:
    def __init__(self, component):
        self._component = component
    
    def operation(self):
        return self._component.operation()

class ConcreteWrapperA(Wrapper):
    def operation(self):
        return f"A({super().operation()})"

class ConcreteWrapperB(Wrapper):
    def operation(self):
        return f"B({super().operation()})"

if __name__ == "__main__":
    component = Component()
    print(component.operation())
    
    wrapped_a = ConcreteWrapperA(component)
    print(wrapped_a.operation())
    
    wrapped_both = ConcreteWrapperB(wrapped_a)
    print(wrapped_both.operation())