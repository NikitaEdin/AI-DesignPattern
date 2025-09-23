class Picture:
    def show(self):
        pass

class ActualPicture(Picture):
    def __init__(self, name):
        self.name = name
        self._load()

    def _load(self):
        print(f"Loading {self.name}")

    def show(self):
        print(f"Displaying {self.name}")

class DelayedPicture(Picture):
    def __init__(self, name):
        self.name = name
        self._actual = None

    def show(self):
        if self._actual is None:
            self._actual = ActualPicture(self.name)
        self._actual.show()

if __name__ == "__main__":
    pic = DelayedPicture("test.jpg")
    pic.show()
    pic.show()