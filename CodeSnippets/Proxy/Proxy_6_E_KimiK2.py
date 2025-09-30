class RealImage:
    def __init__(self, filename):
        self.filename = filename
        self._load_from_disk()
    def _load_from_disk(self):
        print(f"Loading {self.filename}")
    def display(self):
        print(f"Displaying {self.filename}")

class ImageWrapper:
    def __init__(self, filename):
        self.filename = filename
        self._real_image = None
    def display(self):
        if self._real_image is None:
            self._real_image = RealImage(self.filename)
        self._real_image.display()

if __name__ == "__main__":
    img = ImageWrapper("photo.jpg")
    img.display()
    img.display()