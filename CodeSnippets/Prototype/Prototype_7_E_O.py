import copy

class Shape:
    def clone(self):
        return copy.deepcopy(self)

class Circle(Shape):
    def __init__(self, x, y, r, color):
        self.x = x; self.y = y; self.r = r; self.color = color
    def __repr__(self):
        return f"Circle(x={self.x}, y={self.y}, r={self.r}, color={self.color})"

class Rectangle(Shape):
    def __init__(self, x, y, w, h, color):
        self.x = x; self.y = y; self.w = w; self.h = h; self.color = color
    def __repr__(self):
        return f"Rectangle(x={self.x}, y={self.y}, w={self.w}, h={self.h}, color={self.color})"

if __name__ == "__main__":
    c1 = Circle(10, 20, 5, "red")
    c2 = c1.clone(); c2.x = 99; c2.color = "blue"
    r1 = Rectangle(0, 0, 10, 20, "green")
    r2 = r1.clone(); r2.w = 50
    print(c1); print(c2)
    print(r1); print(r2)