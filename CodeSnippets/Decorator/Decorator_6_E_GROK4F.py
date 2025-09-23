class VisualComponent:
    def draw(self):
        pass

class Window(VisualComponent):
    def draw(self):
        print("Drawing window")

class Border(VisualComponent):
    def __init__(self, component):
        self.component = component

    def draw(self):
        print("Drawing border")
        self.component.draw()

if __name__ == "__main__":
    simple_window = Window()
    simple_window.draw()

    bordered_window = Border(simple_window)
    bordered_window.draw()