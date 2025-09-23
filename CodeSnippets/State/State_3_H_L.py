# Define the Shape class
class Shape:
    def __init__(self, color):
        self.color = color

# Define the Rectangle class
class Rectangle(Shape):
    def __init__(self, width, height, color):
        super().__init__(color)
        self.width = width
        self.height = height
    
    # Define a method to calculate the area of the rectangle
    def area(self):
        return self.width * self.height

# Define the Square class
class Square(Rectangle):
    def __init__(self, side_length, color):
        super().__init__(side_length, side_length, color)
    
    # Override the area method to calculate the area of a square
    def area(self):
        return self.width * self.height

# Define the Circle class
class Circle:
    def __init__(self, radius, color):
        self.radius = radius
        self.color = color
    
    # Define a method to calculate the area of the circle
    def area(self):
        return 3.14 * (self.radius ** 2)

# Define the Main class
class Main:
    def __init__(self, shape):
        self.shape = shape
    
    # Define a method to print the color and area of the shape
    def print_color_and_area(self):
        print("The color is", self.shape.color)
        print("The area is", self.shape.area())

# Create an instance of the Main class for each shape
main_rectangle = Main(Rectangle(5, 3, "blue"))
main_square = Main(Square(4, "red"))
main_circle = Main(Circle(2, "green"))

# Call the print_color_and_area method for each instance of the Main class
main_rectangle.print_color_and_area()
main_square.print_color_and_area()
main_circle.print_color_and_area()