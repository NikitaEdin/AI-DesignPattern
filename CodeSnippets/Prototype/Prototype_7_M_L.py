class Shape:
    def __init__(self, color, size):
        self.color = color
        self.size = size

    def draw(self):
        print(f"Drawing {self.color} shape of size {self.size}.")

class Circle(Shape):
    def __init__(self, color, size):
        super().__init__(color, size)

    def draw(self):
        print("Drawing circle.")

class Rectangle(Shape):
    def __init__(self, color, size):
        super().__init__(color, size)

    def draw(self):
        print("Drawing rectangle.")

def main():
    # Create a red circle with size 10.
    circle = Circle("red", 10)
    circle.draw()

    # Create a green rectangle with size 20.
    rectangle = Rectangle("green", 20)
    rectangle.draw()

if __name__ == "__main__":
    main()