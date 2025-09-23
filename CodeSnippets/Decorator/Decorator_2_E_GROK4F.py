class VisualComponent:
    def operation(self):
        pass

class TextView(VisualComponent):
    def operation(self):
        return "TextView content"

class BorderWrapper(VisualComponent):
    def __init__(self, component):
        self.component = component

    def operation(self):
        return self.component.operation() + " surrounded by border"

class ScrollWrapper(VisualComponent):
    def __init__(self, component):
        self.component = component

    def operation(self):
        return self.component.operation() + " inside scrollable area"

if __name__ == "__main__":
    simple_view = TextView()
    bordered_view = BorderWrapper(simple_view)
    scrolled_view = ScrollWrapper(bordered_view)
    print(scrolled_view.operation())