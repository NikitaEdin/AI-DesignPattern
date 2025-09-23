```python
class Director:
    def __init__(self, builder):
        self.builder = builder
    
    def construct(self):
        self.builder.build_pre_condition()
        self.builder.build_block()
        self.builder.build_post_condition()
    
class Builder:
    def __init__(self, name):
        self.name = name
        self.block = []
    
    def build_pre_condition(self):
        print("Building pre-condition")
    
    def build_block(self):
        print("Building block")
    
    def build_post_condition(self):
        print("Building post-condition")

if __name__ == "__main__":
    director = Director(Builder("John"))
    director.construct()
  ```