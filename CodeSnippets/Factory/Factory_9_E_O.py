from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def draw(self): ...

class Circle(Shape):
    def __init__(self, r): self.r = r
    def draw(self): return f"Circle radius {self.r}"

class Square(Shape):
    def __init__(self, s): self.s = s
    def draw(self): return f"Square side {self.s}"

class ShapeMaker:
    def create_shape(self, kind, size):
        if kind == "circle": return Circle(size)
        if kind == "square": return Square(size)
        raise ValueError("Unknown shape")

if __name__ == "__main__":
    m = ShapeMaker()
    a = m.create_shape("circle", 5)
    b = m.create_shape("square", 3)
    print(a.draw())
    print(b.draw())