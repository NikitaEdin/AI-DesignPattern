import copy

class Figure:
    def __init__(self, x=0, y=0, color='black'):
        self.x = x
        self.y = y
        self.color = color

    def clone(self):
        return copy.deepcopy(self)

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def __str__(self):
        return f"Figure at ({self.x}, {self.y}), color: {self.color}"

class Circle(Figure):
    def __init__(self, x=0, y=0, color='black', radius=1):
        super().__init__(x, y, color)
        self.radius = radius

    def __str__(self):
        return f"Circle at ({self.x}, {self.y}), radius: {self.radius}, color: {self.color}"

class Rectangle(Figure):
    def __init__(self, x=0, y=0, color='black', width=1, height=1):
        super().__init__(x, y, color)
        self.width = width
        self.height = height

    def __str__(self):
        return f"Rectangle at ({self.x}, {self.y}), {self.width}x{self.height}, color: {self.color}"

class Group(Figure):
    def __init__(self, x=0, y=0, color='black'):
        super().__init__(x, y, color)
        self.children = []

    def add(self, fig):
        self.children.append(fig)

    def __str__(self):
        return f"Group at ({self.x}, {self.y}), color: {self.color}, with {len(self.children)} children"

class TemplateStore:
    def __init__(self):
        self.templates = {}

    def register(self, name, fig):
        self.templates[name] = fig

    def create_clone(self, name):
        if name in self.templates:
            return self.templates[name].clone()
        raise ValueError(f"Template '{name}' not found")

if __name__ == "__main__":
    store = TemplateStore()

    template_circle = Circle(10, 20, 'red', 5)
    store.register('red_circle', template_circle)

    template_group = Group(0, 0, 'blue')
    template_group.add(Circle(1, 2, 'green', 3))
    template_group.add(Rectangle(4, 5, 'black', 10, 20))
    store.register('complex_group', template_group)

    cloned_circle = store.create_clone('red_circle')
    print("Original circle:", template_circle)
    cloned_circle.move(100, 200)
    print("Cloned circle after move:", cloned_circle)
    print("Original unchanged:", template_circle)

    cloned_group = store.create_clone('complex_group')
    print("\nOriginal group child 0:", template_group.children[0])
    cloned_group.children[0].move(50, 60)
    print("Cloned group child 0 after move:", cloned_group.children[0])
    print("Original group child 0 unchanged:", template_group.children[0])

    print("\nOriginal group:", template_group)
    cloned_group.move(10, 15)
    print("Cloned group after move:", cloned_group)