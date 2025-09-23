class Logger:
    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        print("Logging...")
        return self.func(*args, **kwargs)

@Logger
def say_hello(name):
    print(f"Hello, {name}!")

if __name__ == "__main__":
    say_hello("Alice")