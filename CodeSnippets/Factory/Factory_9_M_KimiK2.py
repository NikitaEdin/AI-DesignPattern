import sys

class Shape:
    def draw(self):
        raise NotImplementedError

class Circle(Shape):
    def draw(self):
        print("Drawing a circle")

class Square(Shape):
    def draw(self):
        print("Drawing a square")

class Triangle(Shape):
    def draw(self):
        print("Drawing a triangle")

class Renderer:
    _catalog = {
        "circle": Circle,
        "square": Square,
        "triangle": Triangle,
    }

    @classmethod
    def create(cls, kind):
        kind = kind.lower()
        if kind not in cls._catalog:
            raise ValueError(f"Unknown shape '{kind}'")
        return cls._catalog[kind]()

if __name__ == "__main__":
    for arg in sys.argv[1:] or ["circle", "square", "triangle"]:
        shape = Renderer.create(arg)
        shape.draw()