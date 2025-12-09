import math


def circle_area(radius: float) -> float:
    """
    Calculate the area of a circle given its radius.
    
    Args:
        radius: The radius of the circle. Must be positive.
        
    Returns:
        The area of the circle. Returns 0.0 for non-positive radius.
    """
    if radius <= 0:
        return 0.0
    return math.pi * radius ** 2


# Example usage
if __name__ == "__main__":
    r = 5.0
    area = circle_area(r)
    print(f"The area for radius {r} is {area:.2f}")