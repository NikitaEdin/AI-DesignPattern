class Component:
    def operation(self):
        return "Base"

class Wrapper:
    def __init__(self, component):
        self._component = component
    
    def operation(self):
        return self._component.operation()

class AddPrefix(Wrapper):
    def operation(self):
        return "Prefix-" + super().operation()

class AddSuffix(Wrapper):
    def operation(self):
        return super().operation() + "-Suffix"

if __name__ == "__main__":
    base = Component()
    print(base.operation())
    
    with_prefix = AddPrefix(base)
    print(with_prefix.operation())
    
    with_both = AddSuffix(AddPrefix(base))
    print(with_both.operation())