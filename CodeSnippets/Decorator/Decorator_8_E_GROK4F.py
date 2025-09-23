class VisualElement:
    def display(self):
        pass

class TextBox(VisualElement):
    def display(self):
        print("Displaying text box content")

class BorderWrapper(VisualElement):
    def __init__(self, element):
        self._element = element

    def display(self):
        print("+-----------------+")
        self._element.display()
        print("+-----------------+")

if __name__ == "__main__":
    simple_box = TextBox()
    simple_box.display()

    bordered_box = BorderWrapper(simple_box)
    bordered_box.display()