class Decorator:
    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)

def decorate(func):
    return Decorator(func)

@decorate
def greet(name):
    print("Hello, " + name + "!")

greet("Alice")  # Output: Hello, Alice!