class Shape():
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def draw(self):
        print("drawing shape...")
    
class Rectangle(Shape):
    def __init__(self, x, y, width, height):
        super().__init__(x, y)
        self.width = width
        self.height = height
    
    def draw(self):
        print("drawing rectangle...")
    
class Circle(Shape):
    def __init__(self, x, y, radius):
        super().__init__(x, y)
        self.radius = radius
    
    def draw(self):
        print("drawing circle...")
    
def main():
    rectangle = Rectangle(10, 20, 50, 75)
    rectangle.draw()
    circle = Circle(30, 40, 20)
    circle.draw()