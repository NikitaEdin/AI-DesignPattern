class Logger:
    def __init__(self, func):
        self.func = func

    def log(self, *args, **kwargs):
        print("Logging...")
        return self.func(*args, **kwargs)

def my_decorated_function(func):
    return Logger(func)

@my_decorated_function
def add(x, y):
    return x + y

if __name__ == "__main__":
    print(add(3, 5))