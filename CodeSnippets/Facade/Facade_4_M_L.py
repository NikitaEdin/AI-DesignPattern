[/INST:  ```
class Shape:
    def draw(self):
        print("Drawing")
    
    def erase(self):
        print("Erasing")
    
class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius
    
    def get_area(self):
        return 3.14 * (self.radius ** 2)
    
    def draw(self):
        print("Drawing circle")
    
class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    def get_area(self):
        return self.width * self.height
    
    def draw(self):
        print("Drawing rectangle")
    
class Ellipse(Shape):
    def __init__(self, radius_x, radius_y):
        self.radius_x = radius_x
        self.radius_y = radius_y
    
    def get_area(self):
        return 3.14 * (self.radius_x ** 2) * (self.radius_y ** 2)
    
    def draw(self):
        print("Drawing ellipse")
        
class ShapeFacade:
    def __init__(self, shape):
        self.shape = shape
    
    def get_area(self):
        return self.shape.get_area()
    
    def draw(self):
        self.shape.draw()
    
    def erase(self):
        self.shape.erase()
    
def main():
    circle = Circle(5)
    rectangle = Rectangle(10, 5)
    ellipse = Ellipse(7, 3)
    
    facade_circle = ShapeFacade(circle)
    facade_rectangle = ShapeFacade(rectangle)
    facade_ellipse = ShapeFacade(ellipse)
    
    print("Circle area:", facade_circle.get_area())
    print("Rectangle area:", facade_rectangle.get_area())
    print("Ellipse area:", facade_ellipse.get_area())
    
    facade_circle.draw()
    facade_rectangle.draw()
    facade_ellipse.draw()
    
    facade_circle.erase()
    facade_rectangle.erase()
    facade_ellipse.erase()