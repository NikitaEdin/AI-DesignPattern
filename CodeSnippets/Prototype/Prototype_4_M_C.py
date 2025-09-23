import copy

class Shape:
    def __init__(self, color, x, y):
        self.color = color
        self.x = x
        self.y = y
    
    def clone(self):
        return copy.deepcopy(self)
    
    def move(self, dx, dy):
        self.x += dx
        self.y += dy
    
    def __str__(self):
        return f"{self.__class__.__name__}(color={self.color}, x={self.x}, y={self.y})"

class Circle(Shape):
    def __init__(self, color, x, y, radius):
        super().__init__(color, x, y)
        self.radius = radius
    
    def __str__(self):
        return f"Circle(color={self.color}, x={self.x}, y={self.y}, radius={self.radius})"

class Rectangle(Shape):
    def __init__(self, color, x, y, width, height):
        super().__init__(color, x, y)
        self.width = width
        self.height = height
    
    def __str__(self):
        return f"Rectangle(color={self.color}, x={self.x}, y={self.y}, width={self.width}, height={self.height})"

class ShapeManager:
    def __init__(self):
        self.templates = {}
    
    def add_template(self, name, shape):
        self.templates[name] = shape
    
    def create_from_template(self, name):
        if name not in self.templates:
            raise ValueError(f"Template '{name}' not found")
        return self.templates[name].clone()

if __name__ == "__main__":
    manager = ShapeManager()
    
    blue_circle = Circle("blue", 0, 0, 5)
    red_rectangle = Rectangle("red", 10, 10, 20, 15)
    
    manager.add_template("default_circle", blue_circle)
    manager.add_template("default_rectangle", red_rectangle)
    
    new_circle = manager.create_from_template("default_circle")
    new_circle.move(100, 50)
    new_circle.color = "green"
    
    new_rect = manager.create_from_template("default_rectangle")
    new_rect.move(-5, 25)
    
    print(f"Original: {blue_circle}")
    print(f"Cloned: {new_circle}")
    print(f"Original: {red_rectangle}")
    print(f"Cloned: {new_rect}")