class MyDecorator:
    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)

def my_decorated_function(text):
    print("Before decoration")
    self.func(text)
    print("After decoration")

my_decorator = MyDecorator(my_decorated_function)

@my_decorator
def say_hello(name):
    print(f"Hello, {name}!")

if __name__ == "__main__":
    say_hello("Alice")