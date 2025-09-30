import copy
from typing import Any, Dict, Optional

class Shape:
    def __init__(self, x: int = 0, y: int = 0, color: str = "black"):
        self.x = x
        self.y = y
        self.color = color

    def duplicate(self) -> "Shape":
        return copy.deepcopy(self)

    def __str__(self):
        return f"{self.__class__.__name__}(x={self.x}, y={self.y}, color={self.color})"

class Circle(Shape):
    def __init__(self, x: int = 0, y: int = 0, color: str = "black", radius: int = 1):
        super().__init__(x, y, color)
        self.radius = radius

    def __str__(self):
        return f"{super().__str__()[:-1]}, radius={self.radius})"

class Rectangle(Shape):
    def __init__(self, x: int = 0, y: int = 0, color: str = "black", width: int = 1, height: int = 1):
        super().__init__(x, y, color)
        self.width = width
        self.height = height

    def __str__(self):
        return f"{super().__str__()[:-1]}, width={self.width}, height={self.height})"

class ShapeCache:
    def __init__(self):
        self._cache: Dict[str, Shape] = {}

    def register(self, key: str, shape: Shape) -> None:
        self._cache[key] = shape

    def retrieve(self, key: str) -> Optional[Shape]:
        cached = self._cache.get(key)
        return cached.duplicate() if cached else None

if __name__ == "__main__":
    cache = ShapeCache()
    cache.register("red_circle", Circle(10, 20, "red", 15))
    cache.register("blue_rect", Rectangle(5, 5, "blue", 30, 20))

    shape1 = cache.retrieve("red_circle")
    shape1.x = 100
    shape1.color = "darkred"

    shape2 = cache.retrieve("red_circle")
    shape3 = cache.retrieve("blue_rect")
    shape3.width = 50

    print(shape1)
    print(shape2)
    print(shape3)