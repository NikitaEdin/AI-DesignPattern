class Shape:
    def __init__(self):
        pass

    def clone(self):
        return self.__class__()

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return 3.14 * self.radius ** 2

    def __str__(self):
        return f"Circle with radius {self.radius}"

class Square(Shape):
    def __init__(self, side_length):
        self.side_length = side_length

    def area(self):
        return self.side_length ** 2

    def __str__(self):
        return f"Square with side length {self.side_length}"

def main():
    circle1 = Circle(5)
    circle2 = circle1.clone()
    square1 = Square(3)
    square2 = square1.clone()

    print(circle1)
    print(circle2)
    print(square1)
    print(square2)

if __name__ == "__main__":
    main()