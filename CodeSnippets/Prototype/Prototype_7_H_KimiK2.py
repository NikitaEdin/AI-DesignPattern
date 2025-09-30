import copy
import uuid

class Shape:
    def __init__(self, x=0, y=0, color='white'):
        self.id = str(uuid.uuid4())
        self.x = x
        self.y = y
        self.color = color
        self._registry = {}

    def register(self, name, obj):
        self._registry[name] = obj

    def unregister(self, name):
        self._registry.pop(name, None)

    def find(self, name):
        return self._registry.get(name)

    def clone(self, **attrs):
        new_obj = copy.deepcopy(self)
        new_obj.id = str(uuid.uuid4())
        for key, value in attrs.items():
            setattr(new_obj, key, value)
        return new_obj

    def __str__(self):
        return f'{self.__class__.__name__}(id={self.id[:8]} x={self.x} y={self.y} color={self.color})'

class Rectangle(Shape):
    def __init__(self, x=0, y=0, color='white', width=100, height=50):
        super().__init__(x, y, color)
        self.width = width
        self.height = height

class Circle(Shape):
    def __init__(self, x=0, y=0, color='white', radius=25):
        super().__init__(x, y, color)
        self.radius = radius

if __name__ == '__main__':
    base = Shape()
    
    original_rect = Rectangle(10, 20, 'blue', 200, 100)
    base.register('blue_rect', original_rect)
    
    original_circle = Circle(50, 50, 'red', 75)
    base.register('red_circle', original_circle)
    
    rect1 = base.find('blue_rect').clone(x=30, y=40, color='green')
    rect2 = base.find('blue_rect').clone(x=100, width=150)
    
    circle1 = base.find('red_circle').clone(y=120, color='yellow')
    circle2 = base.find('red_circle').clone(radius=50, color='purple')
    
    for obj in [original_rect, original_circle, rect1, rect2, circle1, circle2]:
        print(obj)