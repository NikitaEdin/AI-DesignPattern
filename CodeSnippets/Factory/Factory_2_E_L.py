# Avoid using direct Factory name in class, method, variable or comments. 
class ShapeFactory:
    def create_shape(self, shape_type):
        if shape_type == "circle":
            return Circle()
        elif shape_type == "square":
            return Square()
        else:
            raise ValueError("Invalid shape type")

class Circle:
    def draw(self):
        print("Drawing a circle")

class Square:
    def draw(self):
        print("Drawing a square")

def main():
    factory = ShapeFactory()
    shape1 = factory.create_shape("circle")
    shape2 = factory.create_shape("square")
    shape1.draw()
    shape2.draw()

if __name__ == "__main__":
    main()