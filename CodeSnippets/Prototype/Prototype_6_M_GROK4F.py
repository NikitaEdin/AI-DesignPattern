import copy

class Graphic:
    def __init__(self, color='black'):
        self.color = color

    def duplicate(self):
        return copy.deepcopy(self)

class Circle(Graphic):
    def __init__(self, color='black', radius=1, center=(0, 0)):
        super().__init__(color)
        if radius < 0:
            raise ValueError("Radius must be non-negative")
        self.radius = radius
        self.center = center

    def __str__(self):
        return f"Circle at {self.center} with radius {self.radius}, color {self.color}"

class Rectangle(Graphic):
    def __init__(self, color='black', width=1, height=1, position=(0, 0)):
        super().__init__(color)
        if width < 0 or height < 0:
            raise ValueError("Width and height must be non-negative")
        self.width = width
        self.height = height
        self.position = position

    def __str__(self):
        return f"Rectangle at {self.position} size {self.width}x{self.height}, color {self.color}"

if __name__ == "__main__":
    original_circle = Circle('red', 5, (10, 10))
    print(original_circle)
    cloned_circle = original_circle.duplicate()
    cloned_circle.color = 'blue'
    cloned_circle.radius = 3
    print(cloned_circle)
    print(original_circle)
    original_rect = Rectangle('green', 4, 6, (20, 15))
    cloned_rect = original_rect.duplicate()
    cloned_rect.color = 'yellow'
    print(cloned_rect)
    print(original_rect)