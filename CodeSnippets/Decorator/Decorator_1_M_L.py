class GreetingDecorator:
    def __init__(self, func):
        self.func = func

    def say_hello(self, name):
        print(f"Hello, {name}")

class LoggingDecorator:
    def __init__(self, func):
        self.func = func

    def log_call(self, *args, **kwargs):
        print(f"Function called with args: {args} and kwargs: {kwargs}")
        return self.func(*args, **kwargs)

class GreetingLoggerDecorator:
    def __init__(self, func):
        self.func = func

    def log_and_greet(self, name):
        print(f"Logging call to say_hello with name: {name}")
        return self.func(name)

def main():
    greeter = GreetingDecorator()
    logger = LoggingDecorator()
    greeting_logger = GreetingLoggerDecorator()

    # Decorate the greet function with both decorators
    decorated_greet = greeter.say_hello
    decorated_greet = logger.log_call(decorated_greet)
    decorated_greet = greeting_logger.log_and_greet(decorated_greet)

    # Call the decorated function with an argument
    decorated_greet("Alice")

if __name__ == "__main__":
    main()