# Prototype pattern implementation in Python
class Shape(object):
    def __init__(self, color, x, y):
        self.color = color
        self.x = x
        self.y = y
    
    def draw(self):
        print("Drawing a " + self.color + " shape.")
    
    def clone(self):
        return Shape(self.color, self.x, self.y)

class Circle(Shape):
    def __init__(self, color, x, y, radius):
        super().__init__(color, x, y)
        self.radius = radius
    
    def draw(self):
        print("Drawing a " + self.color + " circle.")
    
    def clone(self):
        return Circle(self.color, self.x, self.y, self.radius)

class Rectangle(Shape):
    def __init__(self, color, x, y, width, height):
        super().__init__(color, x, y)
        self.width = width
        self.height = height
    
    def draw(self):
        print("Drawing a " + self.color + " rectangle.")
    
    def clone(self):
        return Rectangle(self.color, self.x, self.y, self.width, self.height)

# Usage example
def main():
    # Create a new circle object and draw it
    my_circle = Circle("red", 10, 20, 5)
    my_circle.draw()
    
    # Clone the circle and change its color
    cloned_circle = my_circle.clone()
    cloned_circle.color = "blue"
    cloned_circle.draw()
    
    # Create a new rectangle object and draw it
    my_rectangle = Rectangle("green", 30, 40, 10, 5)
    my_rectangle.draw()
    
    # Clone the rectangle and change its width
    cloned_rectangle = my_rectangle.clone()
    cloned_rectangle.width = 20
    cloned_rectangle.draw()

if __name__ == "__main__":
    main()