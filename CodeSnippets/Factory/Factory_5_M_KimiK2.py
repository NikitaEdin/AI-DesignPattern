from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def draw(self):
        pass

class Circle(Shape):
    def draw(self):
        return "Drawing a circle"

class Square(Shape):
    def draw(self):
        return "Drawing a square"

class Triangle(Shape):
    def draw(self):
        return "Drawing a triangle"

class ShapeCreator:
    _shapes = {'circle': Circle, 'square': Square, 'triangle': Triangle}

    @classmethod
    def create(cls, type_name):
        if type_name not in cls._shapes:
            raise ValueError(f"Unknown shape: {type_name}")
        return cls._shapes[type_name]()

if __name__ == "__main__":
    for name in ['circle', 'square', 'triangle']:
        shape = ShapeCreator.create(name)
        print(f"{name.capitalize()}: {shape.draw()}")
    try:
        ShapeCreator.create('hexagon')
    except ValueError as e:
        print(e)