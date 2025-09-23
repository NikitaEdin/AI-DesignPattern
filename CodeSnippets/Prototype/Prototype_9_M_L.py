class Shape:
    def __init__(self, color):
        self.color = color
    
    def draw(self):
        print("Drawing a shape")

class Circle(Shape):
    def __init__(self, radius, color):
        super().__init__(color)
        self.radius = radius
    
    def draw(self):
        print("Drawing a circle with radius ", self.radius)

class Rectangle(Shape):
    def __init__(self, width, height, color):
        super().__init__(color)
        self.width = width
        self.height = height
    
    def draw(self):
        print("Drawing a rectangle with width ", self.width, " and height ", self.height)

def main():
    shape1 = Circle(5, "red")
    shape2 = Rectangle(3, 4, "blue")
    shape3 = shape1.clone()
    shape3.color = "green"
    shape1.draw()
    shape2.draw()
    shape3.draw()

if __name__ == "__main__":
    main()