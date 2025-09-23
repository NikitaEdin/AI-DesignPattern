```python
  class Singleton:
    _instance = None

    def __init__(self):
        if not Singleton._instance:
            Singleton._instance = self

    @classmethod
    def instance(cls):
        if not cls._instance:
            cls._instance = Singleton()
        return cls._instance

  # Usage example
  if __name__ == "__main__":
      s1 = Singleton.instance()
      s2 = Singleton.instance()
      print(s1 is s2) # Output: True

      s3 = Singleton() # This will throw an error since the class is a singleton
  ```