from abc import ABC, abstractmethod
from typing import Dict, Type

class Shape(ABC):
    @abstractmethod
    def draw(self) -> str:
        pass
    
    @abstractmethod
    def area(self) -> float:
        pass

class Circle(Shape):
    def __init__(self, radius: float = 1.0):
        self.radius = radius
    
    def draw(self) -> str:
        return f"Drawing a circle with radius {self.radius}"
    
    def area(self) -> float:
        return 3.14159 * self.radius ** 2

class Rectangle(Shape):
    def __init__(self, width: float = 1.0, height: float = 1.0):
        self.width = width
        self.height = height
    
    def draw(self) -> str:
        return f"Drawing a rectangle {self.width}x{self.height}"
    
    def area(self) -> float:
        return self.width * self.height

class ShapeCreator:
    _shapes: Dict[str, Type[Shape]] = {
        'circle': Circle,
        'rectangle': Rectangle
    }
    
    @classmethod
    def create_shape(cls, shape_type: str, **kwargs) -> Shape:
        if shape_type.lower() not in cls._shapes:
            raise ValueError(f"Unknown shape type: {shape_type}")
        
        shape_class = cls._shapes[shape_type.lower()]
        return shape_class(**kwargs)
    
    @classmethod
    def register_shape(cls, name: str, shape_class: Type[Shape]):
        cls._shapes[name.lower()] = shape_class

if __name__ == "__main__":
    creator = ShapeCreator()
    
    circle = creator.create_shape('circle', radius=5.0)
    rectangle = creator.create_shape('rectangle', width=4.0, height=3.0)
    
    print(circle.draw())
    print(f"Area: {circle.area():.2f}")
    
    print(rectangle.draw())
    print(f"Area: {rectangle.area():.2f}")
    
    try:
        invalid_shape = creator.create_shape('triangle')
    except ValueError as e:
        print(f"Error: {e}")