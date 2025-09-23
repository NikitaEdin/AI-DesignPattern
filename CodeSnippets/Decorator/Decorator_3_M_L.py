class Logger(object):
    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        result = self.func(*args, **kwargs)
        print(f"Logging: {result}")
        return result

@Logger
def greet(name):
    return f"Hello, {name}!"

if __name__ == "__main__":
    greet("Alice") # Output: Logging: Hello, Alice!