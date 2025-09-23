class Shape:
    def __init__(self, x, y, color):
        if not isinstance(x, (int, float)) or not isinstance(y, (int, float)):
            raise ValueError("Position coordinates must be numeric")
        self.x = x
        self.y = y
        self.color = color

    def duplicate(self):
        raise NotImplementedError("Subclasses must implement duplicate method")

    def __str__(self):
        return f"Shape at ({self.x}, {self.y}) with color {self.color}"

class Circle(Shape):
    def __init__(self, x, y, color, radius):
        super().__init__(x, y, color)
        if not isinstance(radius, (int, float)) or radius < 0:
            raise ValueError("Radius must be a non-negative number")
        self.radius = radius

    def duplicate(self):
        return Circle(self.x, self.y, self.color, self.radius)

    def __str__(self):
        return f"Circle at ({self.x}, {self.y}) color {self.color} radius {self.radius}"

class Rectangle(Shape):
    def __init__(self, x, y, color, width, height):
        super().__init__(x, y, color)
        if not isinstance(width, (int, float)) or width <= 0:
            raise ValueError("Width must be positive")
        if not isinstance(height, (int, float)) or height <= 0:
            raise ValueError("Height must be positive")
        self.width = width
        self.height = height

    def duplicate(self):
        return Rectangle(self.x, self.y, self.color, self.width, self.height)

    def __str__(self):
        return f"Rectangle at ({self.x}, {self.y}) color {self.color} {self.width}x{self.height}"

if __name__ == "__main__":
    try:
        original_circle = Circle(0, 0, "red", 5)
        cloned_circle = original_circle.duplicate()
        cloned_circle.x = 10
        cloned_circle.radius = 7
        print(f"Original: {original_circle}")
        print(f"Cloned: {cloned_circle}")
        
        original_rect = Rectangle(5, 5, "blue", 10, 20)
        cloned_rect = original_rect.duplicate()
        cloned_rect.color = "green"
        print(f"Original: {original_rect}")
        print(f"Cloned: {cloned_rect}")
    except ValueError as e:
        print(f"Error: {e}")