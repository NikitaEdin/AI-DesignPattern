class Shape:
    def __init__(self):
        self.color = "black"

    def draw(self):
        print("Shape drawn")

class Circle(Shape):
    def __init__(self):
        super().__init__()
        self.radius = 10

    def draw(self):
        print("Circle drawn")

if __name__ == "__main__":
    shape = Shape()
    circle = Circle()

    # Prototype pattern usage
    shape_copy = shape.clone()
    circle_copy = circle.clone()

    shape_copy.color = "red"
    circle_copy.radius = 20

    print(shape.color)   # black
    print(circle.radius) # 20