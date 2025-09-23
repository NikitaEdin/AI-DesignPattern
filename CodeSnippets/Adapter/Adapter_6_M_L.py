def make_adapter(class_):
    class Adapter(class_):
        def __init__(self, wrapped):
            self.wrapped = wrapped
    
        def method1(self, arg1):
            return self.wrapped.method2(arg1)
    
        def method2(self, arg1):
            return self.wrapped.method3(arg1)
    
    return Adapter

class Target:
    def method1(self, arg1):
        print("Target.method1 called with", arg1)
    
    def method2(self, arg1):
        print("Target.method2 called with", arg1)
    
    def method3(self, arg1):
        print("Target.method3 called with", arg1)

class Adapter:
    def __init__(self, wrapped):
        self.wrapped = wrapped
    
    def method1(self, arg1):
        return self.wrapped.method2(arg1)
    
    def method2(self, arg1):
        return self.wrapped.method3(arg1)

target = Target()
adapter = make_adapter(target)
adapter.method1("hello") # Output: Target.method2 called with hello
adapter.method2("world") # Output: Target.method3 called with world