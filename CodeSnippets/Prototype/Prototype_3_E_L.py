class Shape(object):
    def __init__(self, color, x, y):
        self.color = color
        self.x = x
        self.y = y
    
    def draw(self):
        print("Drawing a shape")

class Circle(Shape):
    def __init__(self, color, x, y, radius):
        super().__init__(color, x, y)
        self.radius = radius
    
    def draw(self):
        print("Drawing a circle with radius", self.radius)

class Rectangle(Shape):
    def __init__(self, color, x, y, width, height):
        super().__init__(color, x, y)
        self.width = width
        self.height = height
    
    def draw(self):
        print("Drawing a rectangle with width", self.width, "and height", self.height)

def main():
    circle1 = Circle('red', 10, 20, 5)
    circle1.draw()
    rectangle1 = Rectangle('blue', 30, 40, 10, 5)
    rectangle1.draw()

if __name__ == "__main__":
    main()