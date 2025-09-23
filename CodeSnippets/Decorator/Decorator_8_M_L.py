class MyDecorator:
    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        print("Calling decorated function...")
        return self.func(*args, **kwargs)

def my_decorated_function(x, y):
    return x + y

# Decorate the function
my_decorated_function = MyDecorator(my_decorated_function)

# Call the decorated function
result = my_decorated_function(2, 3)
print(result) # Output: Calling decorated function...6