class Shape:
    def __init__(self, name): self.name = name
    def draw(self): raise NotImplementedError

class Circle(Shape):
    def __init__(self, radius): super().__init__('circle'); self.radius = radius
    def draw(self): return f'Drawing {self.name} with radius {self.radius}'

class Square(Shape):
    def __init__(self, side): super().__init__('square'); self.side = side
    def draw(self): return f'Drawing {self.name} with side {self.side}'

class ShapeMaker:
    def create(self, kind, size):
        if kind == 'circle': return Circle(size)
        if kind == 'square': return Square(size)
        raise ValueError('Unknown shape')

if __name__ == '__main__':
    maker = ShapeMaker()
    s1 = maker.create('circle', 5); s2 = maker.create('square', 3)
    print(s1.draw()); print(s2.draw())