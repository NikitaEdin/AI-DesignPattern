class ImageInterface:
    def display(self):
        pass

class Image(ImageInterface):
    def display(self):
        print("Image displayed")

class ImagePlaceholder(ImageInterface):
    def __init__(self):
        self._real_image = None

    def display(self):
        if self._real_image is None:
            self._real_image = Image()
        self._real_image.display()

if __name__ == "__main__":
    placeholder = ImagePlaceholder()
    placeholder.display()