python
class MyDecorator:
    def __init__(self, func):
        self.func = func
    
    def __call__(self, *args, **kwargs):
        print("Calling the decorated function...")
        return self.func(*args, **kwargs)
        
def my_decorated_function(arg1, arg2):
    print("This is a decorated function.")
    
# Decorate the function with the decorator
my_decorated_function = MyDecorator(my_decorated_function)
 
# Call the decorated function
my_decorated_function("Hello", "World")
print("Done!")

```