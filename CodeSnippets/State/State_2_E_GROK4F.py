class Switch:
    def __init__(self):
        self._handler = OffHandler(self)

    def toggle(self):
        self._handler.handle()

class OffHandler:
    def __init__(self, owner):
        self.owner = owner

    def handle(self):
        print("Switch is off.")
        self.owner._handler = OnHandler(self.owner)

class OnHandler:
    def __init__(self, owner):
        self.owner = owner

    def handle(self):
        print("Switch is on.")
        self.owner._handler = OffHandler(self.owner)

if __name__ == "__main__":
    s = Switch()
    for _ in range(4):
        s.toggle()