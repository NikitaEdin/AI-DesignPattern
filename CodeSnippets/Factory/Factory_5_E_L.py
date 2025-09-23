class ShapeFactory:
    @staticmethod
    def create_shape(name):
        if name == "square":
            return Square()
        elif name == "circle":
            return Circle()
        else:
            raise ValueError("Invalid shape")

class Shape:
    pass

class Square(Shape):
    def area(self):
        return self.side ** 2

class Circle(Shape):
    def area(self):
        return 3.14 * (self.radius ** 2)

if __name__ == "__main__":
    shape = ShapeFactory.create_shape("square")
    print(shape.area())