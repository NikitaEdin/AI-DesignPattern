class Decorator:
    def __init__(self, func):
        self.func = func
    
    def wrapper(self, *args, **kwargs):
        return self.func(*args, **kwargs)
    
    def __call__(self, *args, **kwargs):
        return self.wrapper(*args, **kwargs)

def create_decorator(func):
    return Decorator(func)

@create_decorator
def greet(name):
    print(f"Hello, {name}!")

greet("Alice")  # Output: Hello, Alice!