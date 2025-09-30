import copy

class Shape:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

    def clone(self):
        return copy.deepcopy(self)

    def __str__(self):
        return f"{self.__class__.__name__}(x={self.x}, y={self.y}, color='{self.color}')"


class Rectangle(Shape):
    def __init__(self, x, y, color, width, height):
        super().__init__(x, y, color)
        self.width = width
        self.height = height


if __name__ == "__main__":
    original = Rectangle(10, 20, "blue", 100, 50)
    copy1 = original.clone()
    copy1.x = 30
    copy1.color = "red"
    print(original)
    print(copy1)