class Proxy:
    def __init__(self, obj):
        self.obj = obj
    
    def __getattr__(self, attr):
        return getattr(self.obj, attr)
    
    def __setattr__(self, attr, val):
        setattr(self.obj, attr, val)
    
    def __delattr__(self, attr):
        delattr(self.obj, attr)
    
class ProxyExample:
    def __init__(self):
        self.real_object = RealObject()
        self.proxy = Proxy(self.real_object)
    
    def method_1(self):
        return self.proxy.method_1()
    
    def method_2(self, arg):
        return self.proxy.method_2(arg)
    
class RealObject:
    def method_1(self):
        print("Method 1 called")
        return "Result of Method 1"
    
    def method_2(self, arg):
        print("Method 2 called with argument", arg)
        return "Result of Method 2"
    
if __name__ == "__main__":
    proxy = ProxyExample()
    result = proxy.method_1()
    print("Result of method 1:", result)
    result = proxy.method_2("Argument")
    print("Result of method 2:", result)