class ShapeFactory:
    """
    A factory for creating different shapes.
    """
    
    @staticmethod
    def create_shape(shape_type):
        """
        Creates a new shape based on the given type.
        :param shape_type: The type of shape to create. Must be one of 'circle', 'square', or 'rectangle'.
        :return: A newly created shape object.
        """
        if shape_type == 'circle':
            return Circle()
        elif shape_type == 'square':
            return Square()
        elif shape_type == 'rectangle':
            return Rectangle()
        else:
            raise ValueError('Invalid shape type: {}'.format(shape_type))
    
class Circle:
    """
    A circle shape.
    """
    
    def __init__(self):
        self.radius = 1.0
    
    @property
    def area(self):
        return math.pi * self.radius ** 2
    
    @property
    def perimeter(self):
        return 2 * math.pi * self.radius
    
class Square:
    """
    A square shape.
    """
    
    def __init__(self):
        self.side_length = 1.0
    
    @property
    def area(self):
        return self.side_length ** 2
    
    @property
    def perimeter(self):
        return 4 * self.side_length
    
class Rectangle:
    """
    A rectangle shape.
    """
    
    def __init__(self):
        self.width = 1.0
        self.height = 1.0
    
    @property
    def area(self):
        return self.width * self.height
    
    @property
    def perimeter(self):
        return 2 * (self.width + self.height)
    
def main():
    # Create a circle with a radius of 5:
    circle = ShapeFactory.create_shape('circle')
    circle.radius = 5
    print('Circle area:', circle.area)
    print('Circle perimeter:', circle.perimeter)
    
    # Create a square with a side length of 3:
    square = ShapeFactory.create_shape('square')
    square.side_length = 3
    print('Square area:', square.area)
    print('Square perimeter:', square.perimeter)
    
    # Create a rectangle with a width of 4 and a height of 5:
    rectangle = ShapeFactory.create_shape('rectangle')
    rectangle.width = 4
    rectangle.height = 5
    print('Rectangle area:', rectangle.area)
    print('Rectangle perimeter:', rectangle.perimeter)
```