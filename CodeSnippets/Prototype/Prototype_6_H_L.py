class Shape(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self):
        print("Drawing shape...")

class Rectangle(Shape):
    def __init__(self, x, y, width, height):
        super().__init__(x, y)
        self.width = width
        self.height = height

    def draw(self):
        print("Drawing rectangle...")

class Circle(Shape):
    def __init__(self, x, y, radius):
        super().__init__(x, y)
        self.radius = radius

    def draw(self):
        print("Drawing circle...")

def main():
    # Create a rectangle and a circle as prototypes
    rect1 = Rectangle(10, 20, 50, 60)
    circ1 = Circle(30, 40, 20)

    # Clone the prototypes to create new instances
    rect2 = rect1.clone()
    circ2 = circ1.clone()

    # Draw the cloned shapes
    rect2.draw()
    circ2.draw()

if __name__ == "__main__":
    main()