import copy

class Shape:
    def __init__(self, width, height, color):
        self.width = width
        self.height = height
        self.color = color

    def clone(self):
        return copy.deepcopy(self)

    def __str__(self):
        return f"{self.width}x{self.height} {self.color}"

if __name__ == "__main__":
    original = Shape(10, 20, "red")
    duplicate = original.clone()
    duplicate.color = "blue"
    print(original)
    print(duplicate)