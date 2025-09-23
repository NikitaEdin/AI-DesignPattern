class BitmapImage:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = None
        self._load_image()

    def _load_image(self):
        try:
            print(f"Loading image from {self.file_path}")
            self.data = f"Pixel data loaded for {self.file_path}"
        except Exception as e:
            print(f"Error loading image: {e}")
            self.data = None

    def render(self):
        if self.data:
            print(f"Rendering image: {self.data}")
        else:
            print("Cannot render: image not loaded")

    def get_dimensions(self):
        if self.data:
            return (1920, 1080)
        return (0, 0)


class ImageViewer:
    def __init__(self, file_path):
        self.file_path = file_path
        self._image = None

    def render(self):
        if self._image is None:
            self._image = BitmapImage(self.file_path)
        self._image.render()

    def get_dimensions(self):
        if self._image is None:
            self._image = BitmapImage(self.file_path)
        return self._image.get_dimensions()


if __name__ == "__main__":
    viewer = ImageViewer("example.jpg")
    print("First render:")
    viewer.render()
    print("\nDimensions:")
    print(viewer.get_dimensions())
    print("\nSecond render (no reload):")
    viewer.render()
    print("\nDimensions again:")
    print(viewer.get_dimensions())