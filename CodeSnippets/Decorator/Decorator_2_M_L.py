class Logger:
    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        print("Starting execution of", self.func.__name__)
        result = self.func(*args, **kwargs)
        print("Execution of", self.func.__name__, "completed")
        return result