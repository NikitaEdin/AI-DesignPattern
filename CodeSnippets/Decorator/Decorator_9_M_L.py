class Logger:
    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        print("Calling function...")
        self.func(*args, **kwargs)
        print("Function called.")

def decorated_function(x, y):
    return x + y

decorated = Logger(decorated_function)
result = decorated(2, 3)
print(result)