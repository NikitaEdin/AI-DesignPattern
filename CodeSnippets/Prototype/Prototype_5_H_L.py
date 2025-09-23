class Shape:
    """Abstract class representing a shape"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def move(self, dx, dy):
        """Moves the shape to (dx, dy)"""
        self.x += dx
        self.y += dy

class Circle(Shape):
    """Represents a circle"""
    def __init__(self, x, y, radius):
        super().__init__(x, y)
        self.radius = radius
    
    def area(self):
        """Returns the area of the circle"""
        return math.pi * self.radius ** 2

class Rectangle(Shape):
    """Represents a rectangle"""
    def __init__(self, x, y, width, height):
        super().__init__(x, y)
        self.width = width
        self.height = height
    
    def area(self):
        """Returns the area of the rectangle"""
        return self.width * self.height

class Prototype:
    """Abstract class representing a prototype"""
    def clone(self):
        """Creates a copy of the prototype object"""
        raise NotImplementedError("clone method must be implemented")

class CirclePrototype(Prototype):
    """Represents a circle prototype"""
    def __init__(self, x, y, radius):
        self.shape = Circle(x, y, radius)
    
    def clone(self):
        return CirclePrototype(self.shape.x, self.shape.y, self.shape.radius)

class RectanglePrototype(Prototype):
    """Represents a rectangle prototype"""
    def __init__(self, x, y, width, height):
        self.shape = Rectangle(x, y, width, height)
    
    def clone(self):
        return RectanglePrototype(self.shape.x, self.shape.y, self.shape.width, self.shape.height)

def main():
    # Create a circle prototype
    circle_prototype = CirclePrototype(1, 2, 3)
    
    # Clone the circle prototype and move it to (5, 6)
    circle = circle_prototype.clone()
    circle.move(4, 5)
    
    # Print the area of the cloned circle
    print("Area of the cloned circle:", circle.area())
    
    # Create a rectangle prototype
    rectangle_prototype = RectanglePrototype(1, 2, 3, 4)
    
    # Clone the rectangle prototype and move it to (5, 6)
    rectangle = rectangle_prototype.clone()
    rectangle.move(4, 5)
    
    # Print the area of the cloned rectangle
    print("Area of the cloned rectangle:", rectangle.area())