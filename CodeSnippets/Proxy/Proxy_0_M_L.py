```python
        class Proxy:
            def __init__(self, target):
                self.target = target
            
            def __getattr__(self, name):
                return getattr(self.target, name)
            
            def __setattr__(self, name, value):
                setattr(self.target, name, value)
            
            def __call__(self, *args, **kwargs):
                return self.target(*args, **kwargs)
        
        class RealObject:
            def __init__(self):
                print("RealObject initialized!")
        
        # Usage example
        if __name__ == "__main__":
            obj = RealObject()
            proxy = Proxy(obj)
            proxy.do_something()
            
            # Output: RealObject initialized!
            ```