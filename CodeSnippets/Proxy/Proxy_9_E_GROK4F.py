class BitmapImage:
    def __init__(self, filename):
        self.filename = filename
        self.load()

    def load(self):
        print(f"Loading {self.filename}")

    def display(self):
        print(f"Displaying {self.filename}")

class ImageViewer:
    def __init__(self, filename):
        self.filename = filename
        self.bitmap = None

    def display(self):
        if self.bitmap is None:
            self.bitmap = BitmapImage(self.filename)
        self.bitmap.display()

if __name__ == "__main__":
    viewer = ImageViewer("test.jpg")
    viewer.display()
    viewer.display()