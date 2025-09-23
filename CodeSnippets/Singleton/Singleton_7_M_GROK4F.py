class ApplicationLogger:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, 'initialized'):
            return
        self.initialized = True
        try:
            self.log_file = open('app.log', 'a')
            self.log_file.write("Logger initialized\n")
        except IOError as e:
            raise RuntimeError(f"Failed to open log file: {e}")

    def log(self, message):
        if self.log_file.closed:
            raise ValueError("Cannot log: file is closed")
        try:
            self.log_file.write(f"{message}\n")
            self.log_file.flush()
        except IOError as e:
            raise RuntimeError(f"Failed to write to log: {e}")

    def close(self):
        if not self.log_file.closed:
            try:
                self.log_file.write("Logger closed\n")
                self.log_file.close()
            except IOError as e:
                raise RuntimeError(f"Failed to close log file: {e}")

if __name__ == "__main__":
    logger1 = ApplicationLogger()
    logger2 = ApplicationLogger()
    print(id(logger1) == id(logger2))
    logger1.log("Message from first instance")
    logger2.log("Message from second instance")
    logger1.close()