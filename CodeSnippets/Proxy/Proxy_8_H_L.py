class ImageProxy:
    def __init__(self, image):
        self.image = image
    
    def get_width(self):
        return self.image.get_width()
    
    def get_height(self):
        return self.image.get_height()
    
    def resize(self, width, height):
        return ImageProxy(self.image.resize(width, height))
    
    def rotate(self, angle):
        return ImageProxy(self.image.rotate(angle))