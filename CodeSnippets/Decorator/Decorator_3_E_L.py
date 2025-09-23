```python
    # A simple example of a decorator in Python
    def my_decorator(func):
        def wrapper():
            print("Before calling the function")
            func()
            print("After calling the function")
        return wrapper

    @my_decorator
    def say_hello():
        print("Hello, world!")

    if __name__ == "__main__":
        say_hello()  # Output: Before calling the function. Hello, world! After calling the function.
         ```