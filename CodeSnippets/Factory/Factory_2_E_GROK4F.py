class Shape:
    def draw(self):
        pass

class Circle(Shape):
    def draw(self):
        print("Drawing a circle")

class Square(Shape):
    def draw(self):
        print("Drawing a square")

class ShapeCreator:
    def create_shape(self, shape_type):
        if shape_type == "circle":
            return Circle()
        elif shape_type == "square":
            return Square()
        return None

if __name__ == "__main__":
    creator = ShapeCreator()
    circle = creator.create_shape("circle")
    square = creator.create_shape("square")
    circle.draw()
    square.draw()