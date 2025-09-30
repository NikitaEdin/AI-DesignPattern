class RealImage:
    def __init__(self, filename):
        self.filename = filename
        self.load_from_disk()

    def load_from_disk(self):
        print(f"Loading {self.filename}")

    def display(self):
        print(f"Displaying {self.filename}")


class Image:
    def __init__(self, filename):
        self.real_image = None
        self.filename = filename

    def display(self):
        if self.real_image is None:
            self.real_image = RealImage(self.filename)
        self.real_image.display()


if __name__ == "__main__":
    img = Image("photo.jpg")
    img.display()
    img.display()