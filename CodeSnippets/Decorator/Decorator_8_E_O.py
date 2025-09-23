class Component:
    def render(self):
        raise NotImplementedError
class Text(Component):
    def __init__(self, content):
        self.content = content
    def render(self):
        return self.content
class Wrapper(Component):
    def __init__(self, comp):
        self.comp = comp
    def render(self):
        return self.comp.render()
class Border(Wrapper):
    def render(self):
        return "[" + super().render() + "]"
class Shadow(Wrapper):
    def render(self):
        return "*" + super().render() + "*"
if __name__ == "__main__":
    base = Text("Hello")
    decorated = Shadow(Border(base))
    print(base.render())
    print(decorated.render())