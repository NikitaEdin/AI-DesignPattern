import copy

class Shape:
    def __init__(self, color):
        self.color = color
    
    def set_color(self, new_color):
        self.color = new_color
    
    def get_color(self):
        return self.color

class Rectangle(Shape):
    def __init__(self, length, width, color):
        super().__init__(color)
        self.length = length
        self.width = width
    
    def set_length(self, new_length):
        self.length = new_length
    
    def get_length(self):
        return self.length
    
    def set_width(self, new_width):
        self.width = new_width
    
    def get_width(self):
        return self.width
    
    def get_area(self):
        return self.length * self.width
    
class Circle(Shape):
    def __init__(self, radius, color):
        super().__init__(color)
        self.radius = radius
    
    def set_radius(self, new_radius):
        self.radius = new_radius
    
    def get_radius(self):
        return self.radius
    
    def get_area(self):
        return 3.14 * (self.radius ** 2)

def main():
    # Create a red rectangle
    rect = Rectangle(5, 3, "red")
    print(rect.get_color())  # Output: red
    
    # Create a blue circle
    circ = Circle(2, "blue")
    print(circ.get_color())  # Output: blue
    
    # Clone the rectangle and give it a new length
    rect2 = copy.copy(rect)
    rect2.set_length(10)
    print(rect2.get_area())  # Output: 30
    
    # Clone the circle and give it a new radius
    circ2 = copy.copy(circ)
    circ2.set_radius(5)
    print(circ2.get_area())  # Output: 78.5

if __name__ == "__main__":
    main()