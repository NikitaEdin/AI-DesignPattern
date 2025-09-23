class ProxyClass:
    def __init__(self, real_object):
        self.real_object = real_object

    def proxy_method(self):
        return self.real_object.real_method()

class RealObject:
    def real_method(self):
        return "I am the real object"

def main():
    # Create a proxy class instance
    proxy = ProxyClass(RealObject())

    # Call the proxy method
    result = proxy.proxy_method()

    print(result)

if __name__ == '__main__':
    main()