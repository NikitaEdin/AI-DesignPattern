class ShapePrototype:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def clone(self):
        raise NotImplementedError("Must be implemented in child class")
    
    def draw(self):
        print(f"Drawing {self.__class__.__name__} at ({self.x}, {self.y}).")
    
class CirclePrototype(ShapePrototype):
    def __init__(self, x, y, radius):
        super().__init__(x, y)
        self.radius = radius
    
    def clone(self):
        return CirclePrototype(self.x, self.y, self.radius)
    
class RectanglePrototype(ShapePrototype):
    def __init__(self, x, y, width, height):
        super().__init__(x, y)
        self.width = width
        self.height = height
    
    def clone(self):
        return RectanglePrototype(self.x, self.y, self.width, self.height)
    
class TrianglePrototype(ShapePrototype):
    def __init__(self, x1, y1, x2, y2, x3, y3):
        super().__init__(x1, y1)
        self.x2 = x2
        self.y2 = y2
        self.x3 = x3
        self.y3 = y3
    
    def clone(self):
        return TrianglePrototype(self.x1, self.y1, self.x2, self.y2, self.x3, self.y3)
    
def main():
    shapes = []
    
    # Create circle
    circle = CirclePrototype(5, 6, 7)
    shapes.append(circle)
    
    # Clone circle and translate it by 10
    translated_circle = circle.clone()
    translated_circle.x += 10
    shapes.append(translated_circle)
    
    # Create rectangle
    rectangle = RectanglePrototype(2, 3, 5, 6)
    shapes.append(rectangle)
    
    # Clone rectangle and scale it by 2
    scaled_rectangle = rectangle.clone()
    scaled_rectangle.width *= 2
    scaled_rectangle.height *= 2
    shapes.append(scaled_rectangle)
    
    # Create triangle
    triangle = TrianglePrototype(3, 4, 5, 6, 7, 8)
    shapes.append(triangle)
    
    # Clone triangle and rotate it by 90 degrees
    rotated_triangle = triangle.clone()
    rotated_triangle.x1 += 10
    rotated_triangle.y1 += 10
    shapes.append(rotated_triangle)
    
    # Draw all shapes
    for shape in shapes:
        shape.draw()