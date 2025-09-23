class TextRenderer:
    def render(self):
        raise NotImplementedError

class PlainText(TextRenderer):
    def __init__(self, content):
        self.content = content
    
    def render(self):
        return self.content

class TextWrapper(TextRenderer):
    def __init__(self, text_component):
        if not isinstance(text_component, TextRenderer):
            raise TypeError("Component must be a TextRenderer instance")
        self.component = text_component
    
    def render(self):
        return self.component.render()

class BoldWrapper(TextWrapper):
    def render(self):
        return f"**{self.component.render()}**"

class ItalicWrapper(TextWrapper):
    def render(self):
        return f"*{self.component.render()}*"

class UnderlineWrapper(TextWrapper):
    def render(self):
        return f"_{self.component.render()}_"

class BorderWrapper(TextWrapper):
    def __init__(self, text_component, border_char='|'):
        super().__init__(text_component)
        self.border_char = border_char
    
    def render(self):
        content = self.component.render()
        return f"{self.border_char} {content} {self.border_char}"

if __name__ == "__main__":
    text = PlainText("Hello World")
    print(f"Plain: {text.render()}")
    
    bold_text = BoldWrapper(text)
    print(f"Bold: {bold_text.render()}")
    
    italic_bold = ItalicWrapper(BoldWrapper(text))
    print(f"Italic Bold: {italic_bold.render()}")
    
    fancy_text = BorderWrapper(UnderlineWrapper(ItalicWrapper(BoldWrapper(text))), '#')
    print(f"Fancy: {fancy_text.render()}")