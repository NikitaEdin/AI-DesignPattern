class Shape:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def move(self, delta_x, delta_y):
        self.x += delta_x
        self.y += delta_y
    
    def clone(self):
        return Shape(self.x, self.y)

class Circle(Shape):
    def __init__(self, x, y, radius):
        super().__init__(x, y)
        self.radius = radius
    
    def move(self, delta_x, delta_y):
        super().move(delta_x, delta_y)
        self.radius += math.sqrt(delta_x**2 + delta_y**2)

class Rectangle(Shape):
    def __init__(self, x, y, width, height):
        super().__init__(x, y)
        self.width = width
        self.height = height
    
    def move(self, delta_x, delta_y):
        super().move(delta_x, delta_y)
        self.width += delta_x
        self.height += delta_y

def main():
    circle1 = Circle(0, 0, 5)
    rectangle1 = Rectangle(10, 20, 15, 8)
    
    # Clone the shapes
    circle2 = circle1.clone()
    rectangle2 = rectangle1.clone()
    
    # Move both circles and rectangles
    circle1.move(3, 4)
    rectangle1.move(5, 6)
    
    print("circle1:", circle1.x, ",", circle1.y)
    print("circle2:", circle2.x, ",", circle2.y)
    print("rectangle1:", rectangle1.x, ",", rectangle1.y)
    print("rectangle2:", rectangle2.x, ",", rectangle2.y)

if __name__ == "__main__":
    main()