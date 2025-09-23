# A simple example of a decorator that logs the execution time of a function
import time

def log_execution_time(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"Execution time: {end - start} seconds")
        return result
    return wrapper

# A function to be decorated
def greet(name):
    print(f"Hello, {name}!")

# Decorate the function with the log_execution_time decorator
greet = log_execution_time(greet)

# Call the decorated function with an argument
greet("Alice")