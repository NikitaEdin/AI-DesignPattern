# Simple Decorator Example
def log_time(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__!r} executed in {end - start:.2f} seconds")
        return result
    return wrapper

@log_time
def greet(name):
    print(f"Hello, {name}!")

greet("Alice")