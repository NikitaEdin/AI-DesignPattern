class MyDecorator:
    def __init__(self, func):
        self.func = func
    
    def __call__(self, *args, **kwargs):
        print("Before")
        self.func(*args, **kwargs)
        print("After")
    
def my_function(x, y):
    return x + y
    
# Usage example
my_decorated_function = MyDecorator(my_function)
result = my_decorated_function(2, 3)
print(result)
```
In this code, we define a decorator class `MyDecorator` that takes a function as an argument in its initializer. We then define a method `__call__` that wraps the original function and prints "Before" before calling it, and "After" after calling it.

We also define a function `my_function` that takes two arguments `x` and `y` and returns their sum.

Finally, we create an instance of the decorator class by passing `my_function` to its initializer, and call the resulting object with two arguments (2, 3) to get the result. The output should be "Before" followed by the sum of 2 and 3, which is 5, followed by "After".

Note that the decorator class does not have to be defined in a separate module; it can be defined within the same file as the function it decorates. This makes it easy to test the code without having to create a separate module for the decorator.