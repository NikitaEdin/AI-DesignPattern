# Proxy Design Pattern Implementation in Python

class RealObject:
    def __init__(self, name):
        self.name = name

    def get_name(self):
        return self.name

class ProxyObject:
    def __init__(self, real_object):
        self.real_object = real_object

    def get_name(self):
        return self.real_object.get_name()

# Usage Example in a Main Section
if __name__ == "__main__":
    # Create an instance of the RealObject class
    real_obj = RealObject("John Doe")

    # Create an instance of the ProxyObject class, passing in the real object
    proxy_obj = ProxyObject(real_obj)

    # Call the get_name method on the proxy object to access the name property of the real object
    print(proxy_obj.get_name())