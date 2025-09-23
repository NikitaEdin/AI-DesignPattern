class ImageViewer:
    def __init__(self, filename):
        self.filename = filename
        self.loader = None

    def display(self):
        if self.loader is None:
            self.loader = ImageLoader(self.filename)
        self.loader.show()

class ImageLoader:
    def __init__(self, filename):
        self.filename = filename
        print(f"Loading image: {self.filename}")

    def show(self):
        print(f"Displaying image: {self.filename}")

if __name__ == "__main__":
    viewer = ImageViewer("photo.jpg")
    viewer.display()
    viewer.display()