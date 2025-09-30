class RealImage:
    def __init__(self, filename):
        self.filename = filename
        self.load()

    def load(self):
        print(f"Loading {self.filename}")

    def display(self):
        print(f"Displaying {self.filename}")


class ImageWrapper:
    def __init__(self, filename):
        self.filename = filename
        self._real = None

    def display(self):
        if self._real is None:
            self._real = RealImage(self.filename)
        self._real.display()


if __name__ == "__main__":
    img = ImageWrapper("photo.jpg")
    img.display()