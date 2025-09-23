class Shape:
    def clone(self):
        raise NotImplementedError

class Circle(Shape):
    def __init__(self, radius, color):
        self.radius = radius
        self.color = color
    def clone(self):
        return Circle(self.radius, self.color)
    def __repr__(self):
        return f"Circle(radius={self.radius}, color={self.color!r})"

class Rectangle(Shape):
    def __init__(self, width, height, texture):
        self.width = width
        self.height = height
        self.texture = texture
    def clone(self):
        return Rectangle(self.width, self.height, self.texture)
    def __repr__(self):
        return f"Rectangle(width={self.width}, height={self.height}, texture={self.texture!r})"

if __name__ == "__main__":
    c1 = Circle(5, "red")
    c2 = c1.clone()
    c2.color = "blue"
    r1 = Rectangle(2, 3, "smooth")
    r2 = r1.clone()
    r2.width = 10
    print(c1, c2)
    print(r1, r2)