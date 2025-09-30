import copy

class Shape:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

    def clone(self):
        return copy.deepcopy(self)

    def __str__(self):
        return f"{self.color} shape at ({self.x}, {self.y})"

if __name__ == "__main__":
    original = Shape(10, 20, "red")
    copy1 = original.clone()
    copy1.x = 30
    copy2 = original.clone()
    copy2.color = "blue"
    print(original)
    print(copy1)
    print(copy2)