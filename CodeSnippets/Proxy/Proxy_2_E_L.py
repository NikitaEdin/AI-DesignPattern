class Proxy:
    def __init__(self, target):
        self.target = target
    
    def __getattr__(self, name):
        return getattr(self.target, name)
    
    def __setattr__(self, name, value):
        setattr(self.target, name, value)
    
    def __delattr__(self, name):
        delattr(self.target, name)

class Subject:
    def do_something(self):
        print("I'm the real subject")

if __name__ == "__main__":
    real_subject = Subject()
    proxy = Proxy(real_subject)
    proxy.do_something() # Outputs "I'm the real subject"