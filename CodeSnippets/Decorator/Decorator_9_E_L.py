class MyDecorator:
    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)

def my_decorated(func):
    return MyDecorator(func)

@my_decorated
def add(a, b):
    return a + b

if __name__ == "__main__":
    print(add(3, 4)) # Output: 7