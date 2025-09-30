class RealImage:
    def __init__(self, filename):
        self.filename = filename
        self._load()
    
    def _load(self):
        print(f"Loading {self.filename}")

    def show(self):
        print(f"Displaying {self.filename}")


class ImageViewer:
    def __init__(self, filename):
        self.filename = filename
        self._real = None

    def show(self):
        if self._real is None:
            self._real = RealImage(self.filename)
        self._real.show()


if __name__ == "__main__":
    viewer = ImageViewer("cat.jpg")
    viewer.show()
    viewer.show()