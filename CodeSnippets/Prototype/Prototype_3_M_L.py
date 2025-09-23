class ShapePrototype():
    def __init__(self, color, x_pos, y_pos):
        self.color = color
        self.x_pos = x_pos
        self.y_pos = y_pos

    def set_color(self, color):
        self.color = color

    def set_position(self, x_pos, y_pos):
        self.x_pos = x_pos
        self.y_pos = y_pos

    def get_color(self):
        return self.color

    def get_position(self):
        return self.x_pos, self.y_pos

class Circle(ShapePrototype):
    def __init__(self, radius, color, x_pos, y_pos):
        super().__init__(color, x_pos, y_pos)
        self.radius = radius

    def set_radius(self, radius):
        self.radius = radius

    def get_radius(self):
        return self.radius

class Rectangle(ShapePrototype):
    def __init__(self, width, height, color, x_pos, y_pos):
        super().__init__(color, x_pos, y_pos)
        self.width = width
        self.height = height

    def set_width(self, width):
        self.width = width

    def set_height(self, height):
        self.height = height

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

def main():
    circle1 = Circle(5, "red", 10, 20)
    rectangle1 = Rectangle(10, 5, "blue", 30, 40)
    rectangle2 = Rectangle(10, 5, "green", 50, 60)
    rectangle2.set_width(15)

    print("circle1: ", circle1.get_color(), circle1.get_position())
    print("rectangle1: ", rectangle1.get_color(), rectangle1.get_position(), rectangle1.get_width(), rectangle1.get_height())
    print("rectangle2: ", rectangle2.get_color(), rectangle2.get_position(), rectangle2.get_width(), rectangle2.get_height())

if __name__ == "__main__":
    main()