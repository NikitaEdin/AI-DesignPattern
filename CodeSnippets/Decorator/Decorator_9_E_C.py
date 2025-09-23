class Component:
    def operation(self):
        return "Base"

class Wrapper:
    def __init__(self, component):
        self._component = component
    
    def operation(self):
        return self._component.operation()

class Enhancement(Wrapper):
    def operation(self):
        return f"Enhanced({self._component.operation()})"

class Border(Wrapper):
    def operation(self):
        return f"[{self._component.operation()}]"

if __name__ == "__main__":
    component = Component()
    print(component.operation())
    
    enhanced = Enhancement(component)
    print(enhanced.operation())
    
    bordered = Border(enhanced)
    print(bordered.operation())
    
    double_bordered = Border(Border(component))
    print(double_bordered.operation())