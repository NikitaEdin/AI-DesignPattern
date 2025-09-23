class RealObject:
    def operation(self):
        print("Real Object Operation Called")

class ProxyObject:
    def __init__(self, real_object):
        self.real_object = real_object

    def operation(self):
        if self.real_object is None:
            self.real_object = RealObject()

        return self.real_object.operation()

# Usage example
if __name__ == '__main__':
    proxy = ProxyObject(None)

    print("Calling operation on proxy object")
    result = proxy.operation()

    print(result)