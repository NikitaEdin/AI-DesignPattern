class Logger(object):
    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        print("Calling function")
        return self.func(*args, **kwargs)

@Logger
def add(x, y):
    return x + y

if __name__ == "__main__":
    result = add(3, 5)
    print(result)