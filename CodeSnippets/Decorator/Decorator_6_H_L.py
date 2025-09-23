class DecoratorExample:
    def __init__(self, func):
        self.func = func

    def wrapper(self, *args, **kwargs):
        print("Before")
        self.func(*args, **kwargs)
        print("After")

def decorate(func):
    return DecoratorExample(func).wrapper

@decorate
def foo():
    print("Hello from foo()!")

foo()