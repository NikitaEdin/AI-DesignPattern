class Logger:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
        return cls._instance

    def log(self, message):
        print(f"Log: {message}")

if __name__ == "__main__":
    log1 = Logger()
    log1.log("First message")
    log2 = Logger()
    log2.log("Second message")
    print(log1 is log2)