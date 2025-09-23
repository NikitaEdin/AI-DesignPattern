class MyDecorator:
    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        print("Calling decorated function")
        return self.func(*args, **kwargs)

def my_decorated_function():
    print("This is a decorated function")

# Decorate the function with MyDecorator
my_decorated_function = MyDecorator(my_decorated_function)

# Call the decorated function
my_decorated_function()