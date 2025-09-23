class VisualComponent:
    def display(self):
        pass

class TextView(VisualComponent):
    def display(self):
        print("Displaying text content")

class VisualWrapper(VisualComponent):
    def __init__(self, component):
        self._component = component

    def display(self):
        self._component.display()

class BorderWrapper(VisualWrapper):
    def display(self):
        print("┌───────────────┐")
        super().display()
        print("└───────────────┘")

if __name__ == "__main__":
    simple = TextView()
    simple.display()
    print("\nWith border:")
    bordered = BorderWrapper(simple)
    bordered.display()