import copy

class Shape:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

    def clone(self):
        return copy.deepcopy(self)

    def __str__(self):
        return f"Shape at ({self.x}, {self.y}) with color {self.color}"

if __name__ == "__main__":
    original = Shape(10, 20, "red")
    duplicate = original.clone()
    duplicate.x = 30
    duplicate.color = "blue"
    print(original)
    print(duplicate)