class Component:
    def operation(self):
        return "Basic"

class Wrapper:
    def __init__(self, component):
        self._component = component
    
    def operation(self):
        return self._component.operation()

class ExtraFeature(Wrapper):
    def operation(self):
        return f"Extra({super().operation()})"

class BonusFeature(Wrapper):
    def operation(self):
        return f"Bonus({super().operation()})"

if __name__ == "__main__":
    basic = Component()
    print(basic.operation())
    
    enhanced = ExtraFeature(basic)
    print(enhanced.operation())
    
    super_enhanced = BonusFeature(enhanced)
    print(super_enhanced.operation())