class Logger:
    def __init__(self, logger):
        self.logger = logger

    def log(self, message):
        self.logger.info(message)

def logged_function(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        Logger(logging.getLogger(__name__)).log("Function {0} took {1:.2f} seconds to execute".format(func.__name__, end_time - start_time))
        return result
    return wrapper

@logged_function
def my_function():
    print("Hello from my_function!")

if __name__ == "__main__":
    my_function()