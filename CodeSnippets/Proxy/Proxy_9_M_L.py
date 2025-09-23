class RealObject:
    def operation(self):
        print("Executing real object's operation.")
    
class ProxyObject:
    def __init__(self, real_object):
        self.real_object = real_object
        
    def operation(self):
        if not self.real_object:
            self.real_object = RealObject()
        self.real_object.operation()
    
def main():
    proxy = ProxyObject(None)
    proxy.operation()