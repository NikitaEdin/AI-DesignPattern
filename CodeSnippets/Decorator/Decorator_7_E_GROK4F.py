class Display:
    def show(self):
        pass

class TextDisplay(Display):
    def __init__(self, content):
        self.content = content

    def show(self):
        print(self.content)

class FrameDisplay(Display):
    def __init__(self, wrapped):
        self.wrapped = wrapped

    def show(self):
        print("[")
        self.wrapped.show()
        print("]")

if __name__ == "__main__":
    basic = TextDisplay("Hello, World!")
    basic.show()
    enhanced = FrameDisplay(basic)
    enhanced.show()