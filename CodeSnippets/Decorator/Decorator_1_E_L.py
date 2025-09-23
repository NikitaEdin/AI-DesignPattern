```python
    class MyDecorator(object):
    
      def __init__(self, func):
        self.func = func
    
      def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)
    
    def my_decorated_function(text):
      print("Before: " + text)
    
      # Decorate the function with MyDecorator
      decorated = MyDecorator(my_decorated_function)
    
      # Call the decorated function
      return decorated("After: " + text)
    
    if __name__ == "__main__":
      my_decorated_function("Hello, World!")
        ```