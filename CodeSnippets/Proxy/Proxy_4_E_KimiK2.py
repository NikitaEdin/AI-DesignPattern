class RealImage:
    def __init__(self, filename):
        self.filename = filename
        self._load()

    def _load(self):
        print(f"Loading image: {self.filename}")

    def display(self):
        print(f"Displaying image: {self.filename}")


class ImageWrapper:
    def __init__(self, filename):
        self.filename = filename
        self._real_image = None

    def display(self):
        if self._real_image is None:
            self._real_image = RealImage(self.filename)
        self._real_image.display()


if __name__ == "__main__":
    wrapper = ImageWrapper("photo.jpg")
    wrapper.display()
    wrapper.display()