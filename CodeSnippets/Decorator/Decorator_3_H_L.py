# Decorator Pattern - A Robust Implementation with Advanced Features and Edge Case Handling
# by <Your Name>

class BaseComponent:
    """The base component class that all other components will extend."""

    def __init__(self, name):
        self.name = name

    def get_name(self):
        return self.name

class ConcreteComponentA(BaseComponent):
    """A concrete implementation of the base component."""

    def do_something(self):
        print("ConcreteComponentA: Doing something...")

class ConcreteComponentB(BaseComponent):
    """Another concrete implementation of the base component."""

    def do_something(self):
        print("ConcreteComponentB: Doing something...")

class Decorator:
    """The decorator class that will be used to add new functionality to components."""

    def __init__(self, component):
        self.component = component

    def do_something(self):
        self.component.do_something()

class ConcreteDecoratorA(Decorator):
    """A concrete implementation of the decorator that adds additional functionality."""

    def do_something(self):
        super().do_something()
        print("ConcreteDecoratorA: Doing something...")

class ConcreteDecoratorB(Decorator):
    """Another concrete implementation of the decorator that adds additional functionality."""

    def do_something(self):
        super().do_something()
        print("ConcreteDecoratorB: Doing something...")

def main():
    # Create a component and a decorator
    component = ConcreteComponentA("component A")
    decorator = ConcreteDecoratorA(component)

    # Decorate the component with multiple decorators
    decorator1 = ConcreteDecoratorB(decorator)
    decorator2 = ConcreteDecoratorA(decorator1)

    # Test the decorated component
    print("Testing the decorated component:")
    decorator2.do_something()

if __name__ == "__main__":
    main()