class ShapeFactory:
    def create_shape(self, shape_type):
        if shape_type == "circle":
            return Circle()
        elif shape_type == "square":
            return Square()
        else:
            raise ValueError("Invalid shape type")

class Circle:
    def __init__(self):
        self.radius = 0

    def set_radius(self, radius):
        self.radius = radius

    def get_area(self):
        return 3.14 * (self.radius ** 2)

class Square:
    def __init__(self):
        self.side_length = 0

    def set_side_length(self, side_length):
        self.side_length = side_length

    def get_area(self):
        return self.side_length ** 2

def main():
    shape_factory = ShapeFactory()
    circle = shape_factory.create_shape("circle")
    circle.set_radius(5)
    print(f"Circle area: {circle.get_area()}")

    square = shape_factory.create_shape("square")
    square.set_side_length(6)
    print(f"Square area: {square.get_area()}")

if __name__ == "__main__":
    main()