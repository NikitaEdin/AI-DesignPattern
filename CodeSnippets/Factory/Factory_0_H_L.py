# Robust implementation of the Factory design pattern with advanced features and edge case handling
class ShapeFactory:
    """
    The factory class that creates different shapes based on the input.
    """

    def __init__(self):
        self._shape_map = {
            'circle': Circle,
            'square': Square,
            'rectangle': Rectangle,
            'triangle': Triangle
        }

    def create(self, shape_type: str) -> Shape:
        """
        Creates a new instance of the shape based on the input.
        :param shape_type: The type of shape to be created.
        :return: A newly created shape object.
        """
        if shape_type not in self._shape_map:
            raise ValueError(f'Invalid shape type: {shape_type}')
        return self._shape_map[shape_type]()

class Shape:
    """
    The abstract base class for all shapes.
    """

    def __init__(self):
        pass

    @abstractmethod
    def area(self) -> float:
        """
        Calculates the area of the shape.
        :return: The area of the shape.
        """
        raise NotImplementedError()

class Circle(Shape):
    """
    A circle class that inherits from the Shape base class.
    """

    def __init__(self, radius=1):
        self._radius = radius

    def area(self) -> float:
        return math.pi * self._radius ** 2

class Square(Shape):
    """
    A square class that inherits from the Shape base class.
    """

    def __init__(self, side_length=1):
        self._side_length = side_length

    def area(self) -> float:
        return self._side_length ** 2

class Rectangle(Shape):
    """
    A rectangle class that inherits from the Shape base class.
    """

    def __init__(self, width=1, height=1):
        self._width = width
        self._height = height

    def area(self) -> float:
        return self._width * self._height

class Triangle(Shape):
    """
    A triangle class that inherits from the Shape base class.
    """

    def __init__(self, base=1, height=1):
        self._base = base
        self._height = height

    def area(self) -> float:
        return 0.5 * self._base * self._height

# Usage example
shape_factory = ShapeFactory()
circle = shape_factory.create('circle')
print(f'Circle area: {circle.area()}')
square = shape_factory.create('square')
print(f'Square area: {square.area()}')
rectangle = shape_factory.create('rectangle')
print(f'Rectangle area: {rectangle.area()}')
triangle = shape_factory.create('triangle')
print(f'Triangle area: {triangle.area()}')