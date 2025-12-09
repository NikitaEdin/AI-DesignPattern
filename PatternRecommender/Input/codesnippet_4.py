import math

def calculate_circle_area(radius):
    """Calculates the area of a circle given its radius."""
    if radius <= 0:
        return 0.0
    return math.pi * radius**2

# Example Usage
r = 5.0
area = calculate_circle_area(r)
print(f"The area for radius {r} is {area:.2f}")