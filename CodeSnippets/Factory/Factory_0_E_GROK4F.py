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
    shape1 = creator.create_shape("circle")
    shape1.draw()
    shape2 = creator.create_shape("square")
    shape2.draw()