```python
class Shape(object):
    def __init__(self, color):
        self._color = color
    
    @property
    def color(self):
        return self._color
    
    @color.setter
    def color(self, value):
        self._color = value
        
    def draw(self):
        print("Drawing a shape")
    
class Circle(Shape):
    def __init__(self, radius, color):
        super().__init__(color)
        self.radius = radius
    
    @property
    def area(self):
        return 3.14 * (self.radius ** 2)
    
    def draw(self):
        print("Drawing a circle")
    
class Rectangle(Shape):
    def __init__(self, width, height, color):
        super().__init__(color)
        self.width = width
        self.height = height
    
    @property
    def area(self):
        return self.width * self.height
    
    def draw(self):
        print("Drawing a rectangle")
        
def main():
    circle = Circle(5, "red")
    circle.draw()
    print(circle.area)
    
    rectangle = Rectangle(3, 4, "blue")
    rectangle.draw()
    print(rectangle.area)
    
if __name__ == "__main__":
    main()
   ```