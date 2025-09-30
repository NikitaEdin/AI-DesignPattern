class Text:
    def render(self):
        return "Hello"

class Bold:
    def __init__(self, text):
        self.text = text
    def render(self):
        return f"<b>{self.text.render()}</b>"

class Italic:
    def __init__(self, text):
        self.text = text
    def render(self):
        return f"<i>{self.text.render()}</i>"

if __name__ == "__main__":
    base = Text()
    bold = Bold(base)
    italic_and_bold = Italic(bold)
    print(base.render())
    print(italic_and_bold.render())