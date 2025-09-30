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
    simple = Text()
    styled = Italic(Bold(simple))
    print(styled.render())