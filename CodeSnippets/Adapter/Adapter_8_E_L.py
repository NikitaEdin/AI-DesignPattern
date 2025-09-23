```python
class Target:
    def request(self):
        print("Target class")

class Adapter:
    def __init__(self, target):
        self.target = target
    
    def request_impl(self):
        print("Adapter class")

def main():
    target = Target()
    adapter = Adapter(target)
    adapter.request_impl()

if __name__ == "__main__":
    main()
  ```