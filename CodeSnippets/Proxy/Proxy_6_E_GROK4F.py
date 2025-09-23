class Image:
    def display(self):
        print("Loading and displaying the image.")

class ImageViewer:
    def __init__(self):
        self._image = None

    def display(self):
        if self._image is None:
            self._image = Image()
        self._image.display()

if __name__ == "__main__":
    viewer = ImageViewer()
    viewer.display()
    viewer.display()