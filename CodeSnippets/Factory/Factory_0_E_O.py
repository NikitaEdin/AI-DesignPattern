from abc import ABC, abstractmethod
class Shape(ABC):
    @abstractmethod
    def draw(self) -> str: ...
class Circle(Shape):
    def draw(self) -> str:
        return "Drawing a circle"
class Square(Shape):
    def draw(self) -> str:
        return "Drawing a square"
class Maker:
    def create(self, kind: str) -> Shape:
        if kind == "circle": return Circle()
        if kind == "square": return Square()
        raise ValueError("Unknown shape")
if __name__ == "__main__":
    maker = Maker()
    shapes = [maker.create("circle"), maker.create("square")]
    for s in shapes:
        print(s.draw())