class Circle:
    def draw(self):
        return "Drawing a circle"

class Square:
    def draw(self):
        return "Drawing a square"

class ShapeProvider:
    def create_shape(self, shape_type):
        if shape_type == "circle":
            return Circle()
        elif shape_type == "square":
            return Square()
        return None

if __name__ == "__main__":
    provider = ShapeProvider()
    shape1 = provider.create_shape("circle")
    shape2 = provider.create_shape("square")
    print(shape1.draw())
    print(shape2.draw())