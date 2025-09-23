from abc import ABC, abstractmethod
from copy import copy
import uuid

class Color:
    def __init__(self, red, green, blue):
        self.red = red
        self.green = green
        self.blue = blue

    def __eq__(self, other):
        if not isinstance(other, Color):
            return False
        return (self.red == other.red and
                self.green == other.green and
                self.blue == other.blue)

    def __repr__(self):
        return f"Color({self.red}, {self.green}, {self.blue})"

class UIElement(ABC):
    def __init__(self, name, color):
        self.id = str(uuid.uuid4())
        self.name = name
        self.color = color
        self.parent = None

    @abstractmethod
    def clone(self):
        pass

    def set_parent(self, parent):
        self.parent = parent

    def get_full_name(self):
        if self.parent:
            return f"{self.parent.get_full_name()} > {self.name}"
        return self.name

class Button(UIElement):
    def __init__(self, name, color, label):
        super().__init__(name, color)
        self.label = label

    def clone(self):
        cloned = Button(self.name, Color(self.color.red, self.color.green, self.color.blue), self.label)
        cloned.id = str(uuid.uuid4())
        cloned.set_parent(self.parent)
        return cloned

    def __repr__(self):
        return f"Button(name='{self.name}', label='{self.label}', color={self.color})"

class Panel(UIElement):
    def __init__(self, name, color):
        super().__init__(name, color)
        self.children = []

    def add_child(self, child):
        child.set_parent(self)
        self.children.append(child)

    def clone(self):
        cloned = Panel(self.name, Color(self.color.red, self.color.green, self.color.blue))
        cloned.id = str(uuid.uuid4())
        cloned.set_parent(self.parent)
        for child in self.children:
            cloned_child = child.clone()
            cloned.add_child(cloned_child)
        return cloned

    def __repr__(self):
        return f"Panel(name='{self.name}', children={len(self.children)}, color={self.color})"

class ElementFactory:
    def __init__(self):
        self._registered_elements = {}

    def register(self, key, element):
        if not isinstance(element, UIElement):
            raise ValueError("Only UIElement instances can be registered.")
        self._registered_elements[key] = element

    def create(self, key):
        if key not in self._registered_elements:
            raise KeyError(f"No registered element for key '{key}'.")
        prototype = self._registered_elements[key]
        cloned = prototype.clone()
        # Ensure deep copy integrity by resetting parent chain
        if hasattr(cloned, 'children'):
            self._reset_parents(cloned)
        return cloned

    def _reset_parents(self, panel):
        for child in panel.children:
            child.set_parent(panel)
            if hasattr(child, 'children'):
                self._reset_parents(child)

# Demonstration
if __name__ == "__main__":
    factory = ElementFactory()

    # Register prototypes
    button_proto = Button("BasicButton", Color(255, 0, 0), "Click Me")
    panel_proto = Panel("BasicPanel", Color(0, 255, 0))

    factory.register("button", button_proto)
    factory.register("panel", panel_proto)

    # Create original panel with children
    original_panel = factory.create("panel")
    original_panel.add_child(factory.create("button"))
    original_panel.children[0].label = "Original Label"

    print("Original panel:")
    print(f"  {original_panel}")
    print(f"  Child: {original_panel.children[0]}")
    print(f"  Full name: {original_panel.get_full_name()}")
    print(f"  Child full name: {original_panel.children[0].get_full_name()}")

    # Clone the panel
    cloned_panel = original_panel.clone()

    # Modify clone
    cloned_panel.name = "ClonedPanel"
    if cloned_panel.children:
        cloned_panel.children[0].label = "Cloned Label"

    print("\nCloned panel (modified):")
    print(f"  {cloned_panel}")
    print(f"  Child: {cloned_panel.children[0]}")
    print(f"  Full name: {cloned_panel.get_full_name()}")
    print(f"  Child full name: {cloned_panel.children[0].get_full_name()}")

    # Verify original unchanged
    print("\nOriginal panel (unchanged):")
    print(f"  {original_panel}")
    print(f"  Child: {original_panel.children[0]}")

    # Edge case: Create without prototype
    try:
        factory.create("invalid")
    except KeyError as e:
        print(f"\nEdge case - Invalid key: {e}")

    # Test equality of colors (immutable handling)
    print("\nColor equality test:")
    print(f"Original color == Cloned color: {original_panel.color == cloned_panel.color}")