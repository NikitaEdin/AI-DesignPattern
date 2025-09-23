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

class SecondWrapper(Wrapper):
    def operation(self):
        return f"Modified({super().operation()})"

if __name__ == "__main__":
    base = Component()
    print(base.operation())
    
    enhanced = ConcreteWrapper(base)
    print(enhanced.operation())
    
    modified = SecondWrapper(enhanced)
    print(modified.operation())