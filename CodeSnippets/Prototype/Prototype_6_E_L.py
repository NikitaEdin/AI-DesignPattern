class Shape():
    def __init__(self, color):
        self.color = color

    def get_color(self):
        return self.color

class Circle(Shape):
    def __init__(self, radius, color):
        super().__init__(color)
        self.radius = radius

    def area(self):
        return 3.14 * (self.radius ** 2)

class Rectangle(Shape):
    def __init__(self, length, width, color):
        super().__init__(color)
        self.length = length
        self.width = width

    def area(self):
        return self.length * self.width

def main():
    circle1 = Circle(5, "red")
    rectangle1 = Rectangle(3, 4, "blue")

    print("Circle:", circle1.get_color())
    print("Rectangle:", rectangle1.get_color())

    circle2 = circle1.clone()
    rectangle2 = rectangle1.clone()

    print("Cloned Circle:", circle2.get_color())
    print("Cloned Rectangle:", rectangle2.get_color())

if __name__ == "__main__":
    main()