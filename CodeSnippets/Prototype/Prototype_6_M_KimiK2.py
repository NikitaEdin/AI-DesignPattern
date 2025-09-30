import copy
import uuid

class Shape:
    def __init__(self, color="red"):
        self.color = color
        self.id = str(uuid.uuid4())
    
    def clone(self):
        new_shape = copy.deepcopy(self)
        new_shape.id = str(uuid.uuid4())
        return new_shape
    
    def __str__(self):
        return f"Shape(id={self.id}, color={self.color})"

class Circle(Shape):
    def __init__(self, color="red", radius=5):
        super().__init__(color)
        self.radius = radius
    
    def __str__(self):
        return f"Circle(id={self.id}, color={self.color}, radius={self.radius})"

class Registry:
    def __init__(self):
        self._templates = {}
    
    def add_template(self, key, shape):
        if not isinstance(shape, Shape):
            raise ValueError("Only Shape instances allowed")
        self._templates[key] = shape
    
    def get_by_key(self, key):
        if key not in self._templates:
            raise KeyError(f"Template '{key}' not found")
        return self._templates[key].clone()

if __name__ == "__main__":
    registry = Registry()
    
    original_circle = Circle("blue", 10)
    registry.add_template("blue_circle", original_circle)
    
    clone1 = registry.get_by_key("blue_circle")
    clone2 = registry.get_by_key("blue_circle")
    
    clone1.color = "green"
    clone2.radius = 15
    
    print("Original:", original_circle)
    print("Clone 1:", clone1)
    print("Clone 2:", clone2)