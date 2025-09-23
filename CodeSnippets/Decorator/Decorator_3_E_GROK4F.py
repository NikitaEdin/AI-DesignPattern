class Graphic:
    def display(self):
        pass

class Button(Graphic):
    def display(self):
        print("Display button")

class Frame(Graphic):
    def __init__(self, graphic):
        self.graphic = graphic

    def display(self):
        print("Frame around:")
        self.graphic.display()

class Shadow(Graphic):
    def __init__(self, graphic):
        self.graphic = graphic

    def display(self):
        self.graphic.display()
        print("Add shadow")

if __name__ == "__main__":
    button = Button()
    framed = Frame(button)
    shadowed = Shadow(framed)
    shadowed.display()