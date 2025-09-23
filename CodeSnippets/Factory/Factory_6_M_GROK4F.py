class Shape:
    def __init__(self, color):
        self.color = color

    def draw(self):
        pass

class Circle(Shape):
    def draw(self):
        print(f"Drawing a {self.color} circle")

class Square(Shape):
    def draw(self):
        print(f"Drawing a {self.color} square")

class ShapeCreator:
    def create_shape(self, shape_type, color):
        shape_type = shape_type.lower()
        if shape_type == "circle":
            return Circle(color)
        elif shape_type == "square":
            return Square(color)
        else:
            raise ValueError(f"Unknown shape type: {shape_type}")

if __name__ == "__main__":
    creator = ShapeCreator()
    circle = creator.create_shape("Circle", "red")
    circle.draw()
    square = creator.create_shape("square", "blue")
    square.draw()
    try:
        invalid = creator.create_shape("triangle", "green")
    except ValueError as e:
        print(f"Error: {e}")