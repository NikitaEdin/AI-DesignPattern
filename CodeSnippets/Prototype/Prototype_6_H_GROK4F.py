import abc

class Graphic(abc.ABC):
    def __init__(self):
        self._children = []

    @abc.abstractmethod
    def draw(self):
        pass

    def add(self, child):
        self._children.append(child)

    def remove(self, child):
        if child in self._children:
            self._children.remove(child)

    def deep_clone(self):
        cloned = self._shallow_clone()
        cloned._children = [child.deep_clone() for child in self._children]
        return cloned

    def _shallow_clone(self):
        raise NotImplementedError

class Line(Graphic):
    def __init__(self, start, end):
        super().__init__()
        self.start = start
        self.end = end

    def draw(self):
        print(f"Drawing line from {self.start} to {self.end}")

    def _shallow_clone(self):
        return Line(self.start, self.end)

class Group(Graphic):
    def __init__(self):
        super().__init__()

    def draw(self):
        for child in self._children:
            child.draw()

    def _shallow_clone(self):
        return Group()

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"({self.x}, {self.y})"

class GraphicRegistry:
    def __init__(self):
        self._registered_graphics = {}

    def register_graphic(self, name, graphic):
        if name in self._registered_graphics:
            raise ValueError(f"Name {name} already registered")
        self._registered_graphics[name] = graphic

    def create_graphic(self, name):
        if name not in self._registered_graphics:
            raise KeyError(f"No graphic registered under {name}")
        return self._registered_graphics[name].deep_clone()

def main():
    registry = GraphicRegistry()

    line1 = Line(Point(0, 0), Point(10, 10))
    group1 = Group()
    group1.add(line1)
    line2 = Line(Point(5, 5), Point(15, 15))
    group1.add(line2)

    registry.register_graphic("basic_group", group1)

    cloned_group = registry.create_graphic("basic_group")

    print("Original group drawing:")
    group1.draw()

    print("\nCloned group drawing:")
    cloned_group.draw()

    if cloned_group._children:
        cloned_group._children[0].start.x = 100

    print("\nOriginal after clone modification:")
    group1.draw()

    print("\nCloned after modification:")
    cloned_group.draw()

if __name__ == "__main__":
    main()