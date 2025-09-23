class TextComponent:
    def render(self):
        raise NotImplementedError

class BasicText(TextComponent):
    def __init__(self, text):
        self.text = text
    def render(self):
        return self.text

class Bold(TextComponent):
    def __init__(self, component):
        self.component = component
    def render(self):
        return f"<b>{self.component.render()}</b>"

class Italic(TextComponent):
    def __init__(self, component):
        self.component = component
    def render(self):
        return f"<i>{self.component.render()}</i>"

if __name__ == "__main__":
    base = BasicText("Hello")
    decorated = Bold(Italic(base))
    print(decorated.render())