class Shape:
    def __init__(self, color):
        self.color = color
    
    def get_color(self):
        return self.color
    
    def set_color(self, new_color):
        self.color = new_color
    
class Circle(Shape):
    def __init__(self, radius, color):
        super().__init__(color)
        self.radius = radius
    
    def get_area(self):
        return 3.14 * (self.radius ** 2)

# Usage example
def main():
    # Create a red circle with radius 5
    my_circle = Circle(5, "red")
    print(my_circle.get_area())
    
if __name__ == "__main__":
    main()