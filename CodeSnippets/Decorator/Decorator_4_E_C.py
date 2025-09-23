class Component:
    def operation(self):
        return "Base"

class Wrapper:
    def __init__(self, component):
        self._component = component
    
    def operation(self):
        return self._component.operation()

class EnhancerA(Wrapper):
    def operation(self):
        return f"A({super().operation()})"

class EnhancerB(Wrapper):
    def operation(self):
        return f"B({super().operation()})"

if __name__ == "__main__":
    base = Component()
    print(base.operation())
    
    enhanced_a = EnhancerA(base)
    print(enhanced_a.operation())
    
    enhanced_ab = EnhancerB(enhanced_a)
    print(enhanced_ab.operation())