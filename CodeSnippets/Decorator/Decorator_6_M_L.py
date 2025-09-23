class Logger:
    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        result = self.func(*args, **kwargs)
        print(f"{args} executed in {time.process_time() - start:.2f} seconds")
        return result