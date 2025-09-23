# Decorator Pattern - Implementing a Proxy Class
class Proxy:
    def __init__(self, original):
        self.original = original

    def operation(self):
        print("Proxy Object: Operation")
        # Call the original method
        return self.original.operation()

# Decorator Pattern - Implementing a RealSubject Class
class RealSubject:
    def __init__(self):
        pass

    def operation(self):
        print("Real Subject Object: Operation")
        # Return the result of the original method
        return "Result"

# Test Code
if __name__ == "__main__":
    real_subject = RealSubject()
    proxy = Proxy(real_subject)
    result = proxy.operation()
    print("Result:", result)