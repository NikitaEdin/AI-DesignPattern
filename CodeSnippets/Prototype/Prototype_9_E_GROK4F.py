class Shape:
    def __init__(self, color):
        self.color = color

    def clone(self):
        raise NotImplementedError("Must implement clone method")

class Circle(Shape):
    def __init__(self, color, radius):
        super().__init__(color)
        self.radius = radius

    def clone(self):
        return Circle(self.color, self.radius)

class Square(Shape):
    def __init__(self, color, side):
        super().__init__(color)
        self.side = side

    def clone(self):
        return Square(self.color, self.side)

if __name__ == "__main__":
    original_circle = Circle("red", 5)
    cloned_circle = original_circle.clone()
    print(f"Cloned circle: color={cloned_circle.color}, radius={cloned_circle.radius}")

    original_square = Square("blue", 4)
    cloned_square = original_square.clone()
    print(f"Cloned square: color={cloned_square.color}, side={cloned_square.side}")