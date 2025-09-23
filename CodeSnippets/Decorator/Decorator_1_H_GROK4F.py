class VisualComponent:
    def draw(self):
        pass

    def get_size(self):
        return 0

class Window(VisualComponent):
    def __init__(self, title):
        self._title = title

    def draw(self):
        print(f"Drawing Window: {self._title}")

    def get_size(self):
        return 100

class ComponentWrapper(VisualComponent):
    def __init__(self, component):
        if not isinstance(component, VisualComponent):
            raise ValueError("Wrapped item must be a VisualComponent")
        self._component = component

    def draw(self):
        self._component.draw()

    def get_size(self):
        return self._component.get_size()

class BorderWrapper(ComponentWrapper):
    def __init__(self, component, thickness=1):
        super().__init__(component)
        if thickness < 1:
            raise ValueError("Thickness must be at least 1")
        self._thickness = thickness

    def draw(self):
        print(f"Drawing border of thickness {self._thickness}")
        super().draw()
        print(f"Border complete for thickness {self._thickness}")

    def get_size(self):
        return super().get_size() + (2 * self._thickness)

class ScrollWrapper(ComponentWrapper):
    def __init__(self, component, scroll_type="vertical"):
        super().__init__(component)
        if scroll_type not in ["vertical", "horizontal", "both"]:
            raise ValueError("Invalid scroll type")
        self._scroll_type = scroll_type

    def draw(self):
        super().draw()
        print(f"Adding {self._scroll_type} scroll bars")

    def get_size(self):
        base_size = super().get_size()
        if self._scroll_type in ["vertical", "horizontal"]:
            return base_size + 20
        return base_size + 40

if __name__ == "__main__":
    window = Window("Main Window")
    bordered = BorderWrapper(window, thickness=2)
    scrolled = ScrollWrapper(bordered, scroll_type="both")

    print("Original window:")
    window.draw()
    print(f"Size: {window.get_size()}\n")

    print("With border:")
    bordered.draw()
    print(f"Size: {bordered.get_size()}\n")

    print("With border and scroll:")
    scrolled.draw()
    print(f"Size: {scrolled.get_size()}\n")

    try:
        invalid_wrapper = ScrollWrapper("not a component")
    except ValueError as e:
        print(f"Error handling: {e}")

    try:
        thin_border = BorderWrapper(window, thickness=0)
    except ValueError as e:
        print(f"Error handling: {e}")