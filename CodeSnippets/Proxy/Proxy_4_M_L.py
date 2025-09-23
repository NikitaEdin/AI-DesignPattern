class RealImage:
    def __init__(self, filename):
        self.filename = filename
        self.image = Image.open(filename)

    def display(self):
        self.image.show()

class ProxyImage:
    def __init__(self, filename):
        self.real_image = RealImage(filename)

    def display(self):
        if not self.real_image.image:
            print("Image is not loaded")
        else:
            self.real_image.display()

if __name__ == "__main__":
    proxy_image = ProxyImage("example.jpg")
    proxy_image.display()