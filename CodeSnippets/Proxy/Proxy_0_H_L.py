class RealImage:
    def __init__(self, filename):
        self.filename = filename
        self.image = None

    def load(self):
        # Load the image from file
        self.image = Image.open(self.filename)

    def display(self):
        # Display the image
        self.image.show()

class ProxyImage:
    def __init__(self, filename):
        self.real_image = RealImage(filename)

    def display(self):
        # Check if the image is loaded
        if not self.real_image.image:
            self.real_image.load()

        # Display the image
        self.real_image.display()

# Usage example
if __name__ == "__main__":
    proxy_image = ProxyImage("example.jpg")
    proxy_image.display()