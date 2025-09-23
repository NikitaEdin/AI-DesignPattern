class Shape(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Circle(Shape):
    def __init__(self, x, y, radius):
        super().__init__(x, y)
        self.radius = radius

class Rectangle(Shape):
    def __init__(self, x, y, width, height):
        super().__init__(x, y)
        self.width = width
        self.height = height

def main():
    circle1 = Circle(0, 0, 5)
    rectangle1 = Rectangle(0, 0, 10, 5)
    print("Circle:", circle1)
    print("Rectangle:", rectangle1)

    # Clone the circle
    clone_circle = circle1.clone()
    clone_circle.x = 20
    clone_circle.y = 30
    print("Cloned Circle:", clone_circle)

    # Clone the rectangle
    clone_rectangle = rectangle1.clone()
    clone_rectangle.width = 15
    clone_rectangle.height = 7.5
    print("Cloned Rectangle:", clone_rectangle)

if __name__ == "__main__":
    main()