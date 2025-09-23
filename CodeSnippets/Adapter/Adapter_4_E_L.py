```python
  class Target:
      def request(self):
          print("Target: The target's business logic.")
  
  class Adapter:
      def __init__(self, target):
          self.target = target
  
      def request(self):
          self.target.request()
  
  if __name__ == "__main__":
      # Create a new Target instance
      target = Target()
  
      # Wrap the Target object with an Adapter object
      adapter = Adapter(target)
  
      # Call the request method on the Adapter object
      adapter.request()
  ```