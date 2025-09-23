import copy

class Shape:
    def clone(self):
        return copy.deepcopy(self)

class Circle(Shape):
    def __init__(self, radius, color):
        self.radius = radius
        self.color = color
    def __repr__(self):
        return f"Circle(radius={self.radius}, color={self.color!r})"

if __name__ == "__main__":
    original = Circle(5, "red")
    clone = original.clone()
    clone.radius = 10
    clone.color = "blue"
    print("original:", original)
    print("clone   :", clone)