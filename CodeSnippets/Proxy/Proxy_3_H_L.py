```python
class Proxy(object):
    """
    The Proxy pattern provides a wrapper or agent object that is used to
    interact with another object, called the real subject. The proxy
    adds additional functionality to the real subject's methods without
    altering their behavior.
    """
    
    def __init__(self, real_subject):
        self.real_subject = real_subject
    
    def method1(self):
        # Additional logic before and after calling the real method
        print("Proxy: method1 called")
        self.real_subject.method1()
        print("Proxy: method1 finished")
    
    def method2(self, arg):
        # Additional logic before and after calling the real method
        print("Proxy: method2 called with", arg)
        self.real_subject.method2(arg)
        print("Proxy: method2 finished")
    
    def __getattr__(self, name):
        return getattr(self.real_subject, name)

# Example usage of the Proxy pattern
if __name__ == "__main__":
    # Create a real subject
    real_subject = RealSubject()
    
    # Wrap the real subject with a proxy
    proxy = Proxy(real_subject)
    
    # Call methods on the proxy object, which will call the corresponding
    # method on the real subject after adding additional logic.
    proxy.method1()
    proxy.method2("arg")
       ```