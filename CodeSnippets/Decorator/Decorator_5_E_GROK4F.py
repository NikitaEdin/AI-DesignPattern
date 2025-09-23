class VisualElement:
    def display(self):
        pass

class Button(VisualElement):
    def display(self):
        print("Displaying button")

class Frame(VisualElement):
    def __init__(self, element):
        self._element = element

    def display(self):
        print("Adding frame")
        self._element.display()

class Shadow(VisualElement):
    def __init__(self, element):
        self._element = element

    def display(self):
        self._element.display()
        print("Adding shadow")

if __name__ == "__main__":
    btn = Button()
    framed = Frame(btn)
    shadowed = Shadow(framed)
    shadowed.display()