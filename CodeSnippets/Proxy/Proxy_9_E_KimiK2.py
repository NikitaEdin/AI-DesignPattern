class RealImage:
    def __init__(self, filename):
        self.filename = filename
        self.load_from_disk()

    def load_from_disk(self):
        print(f"Loading {self.filename}")

    def show(self):
        print(f"Displaying {self.filename}")


class ImageDisplay:
    def __init__(self, filename):
        self.filename = filename
        self.image = None

    def show(self):
        if self.image is None:
            self.image = RealImage(self.filename)
        self.image.show()


if __name__ == "__main__":
    display = ImageDisplay("photo.jpg")
    display.show()
    display.show()